"""
Flight search and booking routes
Handles flight operations
"""

from fastapi import APIRouter, HTTPException
from models import FlightSearch, FlightResponse
from database import search_flights, get_flight

router = APIRouter()

@router.post("/search")
async def search_flights_endpoint(search: FlightSearch):
    """Search for available flights"""
    flights = search_flights(
        departure_city=search.departure_city,
        arrival_city=search.arrival_city,
        departure_date=search.departure_date
    )
    
    if flights:
        return {
            "success": True,
            "count": len(flights),
            "flights": flights
        }
    else:
        return {
            "success": True,
            "count": 0,
            "flights": [],
            "message": "No flights found for the given criteria"
        }

@router.get("/{flight_id}")
async def get_flight_endpoint(flight_id: int):
    """Get flight details"""
    flight = get_flight(flight_id)
    
    if flight:
        return {
            "success": True,
            "flight": flight
        }
    else:
        raise HTTPException(status_code=404, detail="Flight not found")

@router.get("/")
async def list_flights():
    """List all available flights"""
    from database import get_connection
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT flight_id, flight_number, airline, departure_city, arrival_city,
               departure_time, arrival_time, available_seats, total_seats, price
        FROM flights
        WHERE available_seats > 0
        ORDER BY departure_time ASC
    """)
    
    flights = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {
        "success": True,
        "count": len(flights),
        "flights": flights
    }
