import sqlite3
import random

current_user = None
current_role = None

#Login funcation
def login_user(email, password):

    global current_user, current_role

    conn = sqlite3.connect("airport.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email, role FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        current_user = user[0]
        current_role = user[1]

        return f"Login successful. Welcome {current_user}"

    return "Invalid email or password"

#logout funcation
def logout_user():

    global current_user, current_role

    if current_user is None:
        return "No user logged in."

    current_user = None
    current_role = None

    return "User logged out successfully."

def search_flights(source, destination, date):

    conn = sqlite3.connect("airport.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT flight_id,flight_number,source,destination,date,available_seats,price
    FROM flights
    WHERE source=? AND destination=? AND date=?
    """,(source,destination,date))

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return "No flights found."

    result = []

    for row in rows:

        result.append(
        f"Flight ID:{row[0]} | Flight:{row[1]} | {row[2]} -> {row[3]} | Date:{row[4]} | Seats:{row[5]} | Price:{row[6]}"
        )

    return "\n".join(result)

def book_flight(flight_id):

    global current_user

    if current_user is None:
        return "Please login first."

    conn = sqlite3.connect("airport.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT available_seats,price FROM flights WHERE flight_id=?",
        (flight_id,)
    )

    flight = cursor.fetchone()

    if not flight:
        conn.close()
        return "Flight not found."

    seats = flight[0]
    price = flight[1]

    if seats <= 0:
        conn.close()
        return "No seats available."

    # prevent double booking
    cursor.execute("""
    SELECT * FROM bookings
    WHERE user_email=? AND flight_id=? AND status='confirmed'
    """,(current_user,flight_id))

    if cursor.fetchone():
        conn.close()
        return "You already booked this flight."

    # create booking
    cursor.execute("""
    INSERT INTO bookings (user_email,flight_id,status)
    VALUES (?,?,?)
    """,(current_user,flight_id,"pending_payment"))

    booking_id = cursor.lastrowid

    # reduce seat
    cursor.execute("""
    UPDATE flights
    SET available_seats = available_seats - 1
    WHERE flight_id=?
    """,(flight_id,))

    conn.commit()
    conn.close()

    return f"Booking created. Booking ID:{booking_id}. Please proceed to payment."

def simulate_payment(booking_id):

    conn = sqlite3.connect("airport.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT flight_id FROM bookings
    WHERE booking_id=? AND status='pending_payment'
    """,(booking_id,))

    booking = cursor.fetchone()

    if not booking:
        conn.close()
        return "Invalid booking."

    success = random.choice([True,True,True,False])

    if success:

        cursor.execute("""
        UPDATE bookings
        SET status='confirmed'
        WHERE booking_id=?
        """,(booking_id,))

        conn.commit()
        conn.close()

        return "Payment successful. Booking confirmed."

    else:

        conn.close()

        return "Payment failed."
    

def cancel_booking(booking_id):

    global current_user

    if current_user is None:
        return "Please login first."

    conn = sqlite3.connect("airport.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT flight_id FROM bookings
    WHERE booking_id=? AND user_email=?
    """,(booking_id,current_user))

    booking = cursor.fetchone()

    if not booking:
        conn.close()
        return "Booking not found."

    flight_id = booking[0]

    cursor.execute("""
    UPDATE bookings
    SET status='cancelled'
    WHERE booking_id=?
    """,(booking_id,))

    cursor.execute("""
    UPDATE flights
    SET available_seats = available_seats + 1
    WHERE flight_id=?
    """,(flight_id,))

    conn.commit()
    conn.close()

    return "Booking cancelled successfully."

def view_user_bookings():

    global current_user

    if current_user is None:
        return "Please login first."

    conn = sqlite3.connect("airport.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT b.booking_id,f.flight_number,f.source,f.destination,f.date,b.status
    FROM bookings b
    JOIN flights f ON b.flight_id=f.flight_id
    WHERE b.user_email=?
    """,(current_user,))

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return "No bookings found."

    result=[]

    for row in rows:

        result.append(
        f"Booking:{row[0]} | Flight:{row[1]} | {row[2]}->{row[3]} | Date:{row[4]} | Status:{row[5]}"
        )

    return "\n".join(result)