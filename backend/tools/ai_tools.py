import os
import google.generativeai as genai
from database import get_db

def get_gemini():
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def get_flights_context():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM flights WHERE available_seats > 0 ORDER BY departure_city, arrival_city, departure_time")
    flights = c.fetchall()
    conn.close()
    lines = []
    for f in flights:
        lines.append(
            f"Flight {f['flight_number']} ({f['airline']}): {f['departure_city']} → {f['arrival_city']}, "
            f"Dep: {f['departure_time']}, Arr: {f['arrival_time']}, "
            f"Price: PKR {f['price']:,}, Seats: {f['available_seats']} available, ID: {f['flight_id']}"
        )
    return "\n".join(lines)

SYSTEM_PROMPT = """You are SkyBot, a friendly airline booking assistant for a Pakistani airline system.

Available flights database:
{flights}

Rules:
- Keep responses SHORT and friendly (2-4 sentences max)
- When showing flights, list them clearly with flight number, route, time, and price
- When user asks to book a flight by number (e.g. "Book PK101"), respond with:
  BOOK_FLIGHT:[flight_number] on a new line, then a friendly confirmation message
- Do NOT ask for extra details like date, class, or number of passengers
- Use PKR currency format
- Be helpful and natural

Examples:
User: "Show flights from Lahore to Karachi"
You: "Here are the available flights from Lahore to Karachi:
✈ PK101 (PIA): 10:00 AM → 11:30 AM | PKR 5,000 | 45 seats
✈ PK102 (PIA): 2:00 PM → 3:30 PM | PKR 5,500 | 42 seats
..."

User: "Book PK101"
You: "BOOK_FLIGHT:PK101
Great choice! I'm booking PK101 for you right now — Lahore to Karachi at 10:00 AM for PKR 5,000. One moment..."
"""

async def chat(message: str, user_id: int) -> dict:
    model = get_gemini()
    flights_ctx = get_flights_context()

    if not model:
        # Fallback without Gemini
        return fallback_chat(message, user_id, flights_ctx)

    prompt = SYSTEM_PROMPT.format(flights=flights_ctx)
    try:
        response = model.generate_content([
            {"role": "user", "parts": [prompt + "\n\nUser: " + message]}
        ])
        text = response.text.strip()
        book_flight = None
        if "BOOK_FLIGHT:" in text:
            lines = text.split("\n")
            for line in lines:
                if line.startswith("BOOK_FLIGHT:"):
                    book_flight = line.replace("BOOK_FLIGHT:", "").strip()
            text = "\n".join(l for l in lines if not l.startswith("BOOK_FLIGHT:")).strip()
        return {"reply": text, "book_flight": book_flight}
    except Exception as e:
        return {"reply": f"Sorry, I encountered an error: {str(e)}", "book_flight": None}

def fallback_chat(message: str, user_id: int, flights_ctx: str) -> dict:
    msg = message.lower().strip()
    conn = get_db()
    c = conn.cursor()

    # Detect booking intent
    import re
    book_match = re.search(r'\b(book|reserve)\b.*?\b([A-Z]{2}\d{3})\b', message, re.IGNORECASE)
    flight_match = re.search(r'\b([A-Z]{2}\d{3})\b', message, re.IGNORECASE)

    if book_match or ("book" in msg and flight_match):
        fn = (book_match.group(2) if book_match else flight_match.group(1)).upper()
        c.execute("SELECT * FROM flights WHERE UPPER(flight_number)=? AND available_seats>0", (fn,))
        f = c.fetchone()
        conn.close()
        if f:
            return {
                "reply": f"✈️ Booking {fn} — {f['departure_city']} to {f['arrival_city']} at {f['departure_time']} for PKR {f['price']:,}. Just a moment...",
                "book_flight": fn
            }
        return {"reply": f"Sorry, I couldn't find flight {fn} or it has no available seats.", "book_flight": None}

    # Search intent
    cities = ["lahore", "karachi", "islamabad", "peshawar"]
    found = [c2 for c2 in cities if c2 in msg]

    if len(found) >= 2:
        c.execute("""SELECT * FROM flights WHERE LOWER(departure_city) LIKE ? AND LOWER(arrival_city) LIKE ? AND available_seats>0 ORDER BY price""",
                  (f"%{found[0]}%", f"%{found[1]}%"))
    elif len(found) == 1:
        c.execute("""SELECT * FROM flights WHERE (LOWER(departure_city) LIKE ? OR LOWER(arrival_city) LIKE ?) AND available_seats>0 ORDER BY departure_city, price""",
                  (f"%{found[0]}%", f"%{found[0]}%"))
    elif any(w in msg for w in ["all flights", "show flights", "available flights", "list flights"]):
        c.execute("SELECT * FROM flights WHERE available_seats>0 ORDER BY departure_city, price")
    else:
        conn.close()
        return {"reply": "Hi! I can help you find and book flights. Try asking: 'Show flights from Lahore to Karachi' or 'Book PK101'.", "book_flight": None}

    flights = c.fetchall()
    conn.close()

    if not flights:
        return {"reply": "No available flights found for that route.", "book_flight": None}

    lines = [f"Here are the available flights:\n"]
    for f in flights:
        lines.append(f"✈ {f['flight_number']} ({f['airline']}): {f['departure_city']} → {f['arrival_city']}, {f['departure_time']} - {f['arrival_time']} | PKR {f['price']:,} | {f['available_seats']} seats")
    lines.append(f"\nTo book, type: 'Book [flight number]'")
    return {"reply": "\n".join(lines), "book_flight": None}
