from fastapi import APIRouter, HTTPException
from database import get_db
from models import BookingCreate
import random, string

router = APIRouter()

def gen_ref():
    return "BK" + "".join(random.choices(string.digits, k=6))

@router.get("/user/{user_id}")
def get_user_bookings(user_id: int):
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT b.*, f.flight_number, f.airline, f.departure_city, f.arrival_city,
               f.departure_time, f.arrival_time, f.departure_date
        FROM bookings b
        JOIN flights f ON b.flight_id = f.flight_id
        WHERE b.user_id=? AND b.status='booked'
        ORDER BY b.booking_date DESC
    """, (user_id,))
    bookings = [dict(row) for row in c.fetchall()]
    conn.close()
    return bookings

@router.post("/create")
def create_booking(data: BookingCreate):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM flights WHERE flight_id=? AND available_seats > 0", (data.flight_id,))
    flight = c.fetchone()
    if not flight:
        conn.close()
        raise HTTPException(400, "Flight not found or no seats available")

    # Generate unique seat
    taken = set()
    c.execute("SELECT seat_number FROM bookings WHERE flight_id=? AND status='booked'", (data.flight_id,))
    for row in c.fetchall():
        taken.add(row["seat_number"])
    rows = list("ABCDEF")
    seat = None
    for num in range(1, 51):
        for row in rows:
            s = f"{num}{row}"
            if s not in taken:
                seat = s
                break
        if seat:
            break

    ref = gen_ref()
    while True:
        c.execute("SELECT booking_id FROM bookings WHERE booking_reference=?", (ref,))
        if not c.fetchone():
            break
        ref = gen_ref()

    c.execute("""
        INSERT INTO bookings (user_id, flight_id, passenger_name, seat_number, booking_reference, price_paid)
        VALUES (?,?,?,?,?,?)
    """, (data.user_id, data.flight_id, data.passenger_name, seat, ref, flight["price"]))

    c.execute("UPDATE flights SET available_seats = available_seats - 1 WHERE flight_id=?", (data.flight_id,))
    conn.commit()
    conn.close()

    return {
        "message": "Booking created successfully",
        "booking_reference": ref,
        "seat_number": seat,
        "price_paid": flight["price"],
        "flight_number": flight["flight_number"]
    }

@router.post("/cancel/{booking_id}")
def cancel_booking(booking_id: int):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM bookings WHERE booking_id=? AND status='booked'", (booking_id,))
    booking = c.fetchone()
    if not booking:
        conn.close()
        raise HTTPException(404, "Booking not found")
    c.execute("UPDATE bookings SET status='cancelled' WHERE booking_id=?", (booking_id,))
    c.execute("UPDATE flights SET available_seats = available_seats + 1 WHERE flight_id=?", (booking["flight_id"],))
    conn.commit()
    conn.close()
    return {"message": "Booking cancelled successfully"}
