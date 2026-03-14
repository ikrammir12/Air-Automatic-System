"""
SQLite3 Database Setup and Operations
Handles all database operations for the Airline Booking System
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import hashlib
import json

DATABASE_PATH = "airline_system.db"

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """Initialize database with tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Flights table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number TEXT UNIQUE NOT NULL,
            airline TEXT NOT NULL,
            departure_city TEXT NOT NULL,
            arrival_city TEXT NOT NULL,
            departure_time TIMESTAMP NOT NULL,
            arrival_time TIMESTAMP NOT NULL,
            total_seats INTEGER NOT NULL,
            available_seats INTEGER NOT NULL,
            price REAL NOT NULL,
            aircraft_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Bookings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            flight_id INTEGER NOT NULL,
            booking_reference TEXT UNIQUE NOT NULL,
            passenger_name TEXT NOT NULL,
            seat_number TEXT,
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'confirmed',
            price_paid REAL NOT NULL,
            is_return BOOLEAN DEFAULT FALSE,
            return_flight_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (flight_id) REFERENCES flights(flight_id),
            FOREIGN KEY (return_flight_id) REFERENCES flights(flight_id)
        )
    """)
    
    # Sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    conn.commit()
    conn.close()
    
    # Insert sample data
    insert_sample_data()

def insert_sample_data():
    """Insert sample flights and user data for testing"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        return  # Data already exists
    
    # Sample users
    sample_users = [
        ("user1@example.com", hash_password("password123"), "Ahmed Khan", "03001234567"),
        ("user2@example.com", hash_password("password123"), "Fatima Ali", "03009876543"),
        ("user3@example.com", hash_password("password123"), "Hassan Ibrahim", "03005555555"),
    ]
    
    for email, pwd_hash, name, phone in sample_users:
        try:
            cursor.execute(
                "INSERT INTO users (email, password, full_name, phone) VALUES (?, ?, ?, ?)",
                (email, pwd_hash, name, phone)
            )
        except sqlite3.IntegrityError:
            pass
    
    # Sample flights
    now = datetime.now()
    
    sample_flights = [
        # Lahore to Karachi
        ("PK101", "Pakistan Airlines", "Lahore", "Karachi", 
         now + timedelta(days=1, hours=8), now + timedelta(days=1, hours=10), 180, 180, 8500),
        ("PK102", "Airblue", "Lahore", "Karachi",
         now + timedelta(days=1, hours=14), now + timedelta(days=1, hours=16), 150, 150, 7800),
        ("PK103", "SereneAir", "Lahore", "Karachi",
         now + timedelta(days=2, hours=10), now + timedelta(days=2, hours=12), 100, 100, 6500),
        
        # Karachi to Lahore
        ("PK201", "Pakistan Airlines", "Karachi", "Lahore",
         now + timedelta(days=1, hours=11), now + timedelta(days=1, hours=13), 180, 180, 8500),
        ("PK202", "Airblue", "Karachi", "Lahore",
         now + timedelta(days=1, hours=16), now + timedelta(days=1, hours=18), 150, 150, 7800),
        
        # Lahore to Islamabad
        ("PK301", "Pakistan Airlines", "Lahore", "Islamabad",
         now + timedelta(days=1, hours=6), now + timedelta(days=1, hours=7), 120, 120, 4500),
        ("PK302", "Airblue", "Lahore", "Islamabad",
         now + timedelta(days=2, hours=9), now + timedelta(days=2, hours=10), 120, 120, 4200),
        
        # Islamabad to Lahore
        ("PK401", "Pakistan Airlines", "Islamabad", "Lahore",
         now + timedelta(days=1, hours=9), now + timedelta(days=1, hours=10), 120, 120, 4500),
        ("PK402", "Airblue", "Islamabad", "Lahore",
         now + timedelta(days=2, hours=15), now + timedelta(days=2, hours=16), 120, 120, 4200),
        
        # Karachi to Islamabad
        ("PK501", "Pakistan Airlines", "Karachi", "Islamabad",
         now + timedelta(days=1, hours=12), now + timedelta(days=1, hours=15), 160, 160, 9500),
        ("PK502", "Airblue", "Karachi", "Islamabad",
         now + timedelta(days=2, hours=11), now + timedelta(days=2, hours=14), 140, 140, 8800),
        
        # Islamabad to Karachi
        ("PK601", "Pakistan Airlines", "Islamabad", "Karachi",
         now + timedelta(days=1, hours=13), now + timedelta(days=1, hours=16), 160, 160, 9500),
        ("PK602", "Airblue", "Islamabad", "Karachi",
         now + timedelta(days=2, hours=16), now + timedelta(days=2, hours=19), 140, 140, 8800),
    ]
    
    for flight in sample_flights:
        try:
            cursor.execute(
                """INSERT INTO flights 
                   (flight_number, airline, departure_city, arrival_city, 
                    departure_time, arrival_time, total_seats, available_seats, price, aircraft_type)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                flight + ("Boeing 737",)
            )
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()

# ============= USER OPERATIONS =============

def user_exists(email: str) -> bool:
    """Check if user exists by email"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def register_user(email: str, password: str, full_name: str, phone: str = "") -> Dict:
    """Register a new user"""
    if user_exists(email):
        return {"success": False, "message": "User already exists"}
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """INSERT INTO users (email, password, full_name, phone) 
               VALUES (?, ?, ?, ?)""",
            (email, hash_password(password), full_name, phone)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return {
            "success": True,
            "message": "User registered successfully",
            "user_id": user_id
        }
    except Exception as e:
        conn.close()
        return {"success": False, "message": str(e)}

def authenticate_user(email: str, password: str) -> Dict:
    """Authenticate user login"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT user_id, full_name, email FROM users WHERE email = ? AND password = ?",
        (email, hash_password(password))
    )
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "success": True,
            "user_id": result["user_id"],
            "full_name": result["full_name"],
            "email": result["email"]
        }
    return {"success": False, "message": "Invalid credentials"}

def get_user(user_id: int) -> Optional[Dict]:
    """Get user information"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, full_name, email, phone FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return dict(result) if result else None

# ============= FLIGHT OPERATIONS =============

def search_flights(departure_city: str, arrival_city: str, departure_date: str = None) -> List[Dict]:
    """Search for available flights"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT flight_id, flight_number, airline, departure_city, arrival_city,
               departure_time, arrival_time, available_seats, total_seats, price
        FROM flights
        WHERE departure_city = ? AND arrival_city = ?
        AND available_seats > 0
    """
    params = [departure_city, arrival_city]
    
    if departure_date:
        query += " AND DATE(departure_time) = ?"
        params.append(departure_date)
    
    query += " ORDER BY departure_time ASC"
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]

def get_flight(flight_id: int) -> Optional[Dict]:
    """Get flight details"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT flight_id, flight_number, airline, departure_city, arrival_city,
               departure_time, arrival_time, available_seats, total_seats, price
        FROM flights
        WHERE flight_id = ?
    """, (flight_id,))
    result = cursor.fetchone()
    conn.close()
    
    return dict(result) if result else None

# ============= BOOKING OPERATIONS =============

def book_flight(user_id: int, flight_id: int, passenger_name: str, return_flight_id: int = None) -> Dict:
    """Book a flight"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get flight details
    cursor.execute("SELECT price, available_seats FROM flights WHERE flight_id = ?", (flight_id,))
    flight = cursor.fetchone()
    
    if not flight or flight["available_seats"] <= 0:
        conn.close()
        return {"success": False, "message": "Flight not available"}
    
    try:
        # Generate booking reference
        booking_ref = f"BK{user_id}{flight_id}{datetime.now().timestamp()}".replace(".", "")[:10]
        
        # Create booking
        cursor.execute("""
            INSERT INTO bookings 
            (user_id, flight_id, booking_reference, passenger_name, price_paid, return_flight_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, flight_id, booking_ref, passenger_name, flight["price"], return_flight_id))
        
        # Update available seats
        cursor.execute(
            "UPDATE flights SET available_seats = available_seats - 1 WHERE flight_id = ?",
            (flight_id,)
        )
        
        # If return flight, also book it
        if return_flight_id:
            cursor.execute("SELECT price FROM flights WHERE flight_id = ?", (return_flight_id,))
            return_flight = cursor.fetchone()
            
            cursor.execute("""
                INSERT INTO bookings 
                (user_id, flight_id, booking_reference, passenger_name, price_paid, is_return)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, return_flight_id, booking_ref, passenger_name, return_flight["price"], True))
            
            cursor.execute(
                "UPDATE flights SET available_seats = available_seats - 1 WHERE flight_id = ?",
                (return_flight_id,)
            )
        
        conn.commit()
        booking_id = cursor.lastrowid
        conn.close()
        
        return {
            "success": True,
            "booking_id": booking_id,
            "booking_reference": booking_ref,
            "message": "Flight booked successfully"
        }
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"success": False, "message": str(e)}

def get_user_bookings(user_id: int) -> List[Dict]:
    """Get all bookings for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT b.booking_id, b.booking_reference, b.passenger_name, b.booking_date,
               b.status, b.price_paid, f.flight_number, f.airline,
               f.departure_city, f.arrival_city, f.departure_time, f.arrival_time
        FROM bookings b
        JOIN flights f ON b.flight_id = f.flight_id
        WHERE b.user_id = ? AND b.status = 'confirmed'
        ORDER BY f.departure_time ASC
    """, (user_id,))
    
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]

def cancel_booking(booking_id: int) -> Dict:
    """Cancel a booking"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get flight_id
        cursor.execute("SELECT flight_id FROM bookings WHERE booking_id = ?", (booking_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return {"success": False, "message": "Booking not found"}
        
        flight_id = result["flight_id"]
        
        # Update booking status
        cursor.execute("UPDATE bookings SET status = 'cancelled' WHERE booking_id = ?", (booking_id,))
        
        # Restore available seats
        cursor.execute(
            "UPDATE flights SET available_seats = available_seats + 1 WHERE flight_id = ?",
            (flight_id,)
        )
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Booking cancelled successfully"}
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"success": False, "message": str(e)}

def get_db():
    """Dependency for FastAPI"""
    return get_connection()
