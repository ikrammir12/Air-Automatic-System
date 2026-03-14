"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ============= USER MODELS =============

class UserRegister(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """User response model"""
    user_id: int
    full_name: str
    email: str
    phone: Optional[str] = None

# ============= FLIGHT MODELS =============

class FlightResponse(BaseModel):
    """Flight response model"""
    flight_id: int
    flight_number: str
    airline: str
    departure_city: str
    arrival_city: str
    departure_time: str
    arrival_time: str
    available_seats: int
    total_seats: int
    price: float

class FlightSearch(BaseModel):
    """Flight search request"""
    departure_city: str
    arrival_city: str
    departure_date: Optional[str] = None

# ============= BOOKING MODELS =============

class BookingRequest(BaseModel):
    """Booking request model"""
    flight_id: int
    passenger_name: str
    return_flight_id: Optional[int] = None

class BookingResponse(BaseModel):
    """Booking response model"""
    booking_id: int
    booking_reference: str
    passenger_name: str
    booking_date: str
    status: str
    price_paid: float
    flight_number: str
    airline: str
    departure_city: str
    arrival_city: str
    departure_time: str
    arrival_time: str

# ============= AI ASSISTANT MODELS =============

class AIMessage(BaseModel):
    """AI assistant message"""
    user_id: int
    message: str
    session_context: Optional[dict] = None

class AIResponse(BaseModel):
    """AI assistant response"""
    response: str
    tool_calls: Optional[List[dict]] = None
    data: Optional[dict] = None
