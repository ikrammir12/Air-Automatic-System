from fastapi import APIRouter
from database import get_db

router = APIRouter()

@router.get("/all")
def get_all_flights():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM flights WHERE available_seats > 0 ORDER BY departure_city, arrival_city, departure_time")
    flights = [dict(row) for row in c.fetchall()]
    conn.close()
    return flights

@router.get("/search")
def search_flights(from_city: str = None, to_city: str = None):
    conn = get_db()
    c = conn.cursor()
    query = "SELECT * FROM flights WHERE available_seats > 0"
    params = []
    if from_city:
        query += " AND LOWER(departure_city) LIKE LOWER(?)"
        params.append(f"%{from_city}%")
    if to_city:
        query += " AND LOWER(arrival_city) LIKE LOWER(?)"
        params.append(f"%{to_city}%")
    query += " ORDER BY price"
    c.execute(query, params)
    flights = [dict(row) for row in c.fetchall()]
    conn.close()
    return flights
