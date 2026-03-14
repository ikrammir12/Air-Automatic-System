"""
Booking management routes
Handles user bookings
"""

from fastapi import APIRouter, HTTPException
from models import BookingRequest
from database import book_flight, get_user_bookings, cancel_booking

router = APIRouter()

@router.post("/create")
async def create_booking(booking: BookingRequest, user_id: int):
    """Create a new flight booking"""
    result = book_flight(
        user_id=user_id,
        flight_id=booking.flight_id,
        passenger_name=booking.passenger_name,
        return_flight_id=booking.return_flight_id
    )
    
    if result["success"]:
        return {
            "success": True,
            "message": result["message"],
            "booking_id": result["booking_id"],
            "booking_reference": result["booking_reference"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["message"])

@router.get("/user/{user_id}")
async def get_bookings(user_id: int):
    """Get all bookings for a user"""
    bookings = get_user_bookings(user_id)
    
    return {
        "success": True,
        "count": len(bookings),
        "bookings": bookings
    }

@router.delete("/{booking_id}")
async def delete_booking(booking_id: int):
    """Cancel a booking"""
    result = cancel_booking(booking_id)
    
    if result["success"]:
        return {
            "success": True,
            "message": result["message"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["message"])

@router.get("/")
async def list_all_bookings():
    """List all bookings (admin endpoint)"""
    from database import get_connection
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT b.booking_id, b.booking_reference, b.passenger_name, 
               b.booking_date, b.status, b.price_paid,
               f.flight_number, f.airline, f.departure_city, f.arrival_city,
               f.departure_time, f.arrival_time, u.full_name
        FROM bookings b
        JOIN flights f ON b.flight_id = f.flight_id
        JOIN users u ON b.user_id = u.user_id
        WHERE b.status = 'confirmed'
        ORDER BY f.departure_time ASC
    """)
    
    bookings = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {
        "success": True,
        "count": len(bookings),
        "bookings": bookings
    }
