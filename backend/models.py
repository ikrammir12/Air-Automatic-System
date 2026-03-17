from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class BookingCreate(BaseModel):
    user_id: int
    flight_id: int
    passenger_name: str

class ChatMessage(BaseModel):
    message: str
    user_id: int
