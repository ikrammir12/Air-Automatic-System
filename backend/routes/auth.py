"""
Authentication routes
Handles user login and registration
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from models import UserLogin, UserRegister, UserResponse
from database import authenticate_user, register_user, get_user
import secrets
import sqlite3

router = APIRouter()

# Simple session storage (in production, use JWT or similar)
sessions = {}

@router.post("/register")
async def register(user_data: UserRegister):
    """Register a new user"""
    result = register_user(
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name,
        phone=user_data.phone or ""
    )
    
    if result["success"]:
        return {
            "success": True,
            "message": result["message"],
            "user_id": result["user_id"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["message"])

@router.post("/login")
async def login(user_data: UserLogin):
    """Authenticate user login"""
    result = authenticate_user(email=user_data.email, password=user_data.password)
    
    if result["success"]:
        # Generate session token
        token = secrets.token_urlsafe(32)
        sessions[token] = {
            "user_id": result["user_id"],
            "email": result["email"],
            "full_name": result["full_name"]
        }
        
        return {
            "success": True,
            "message": "Login successful",
            "user_id": result["user_id"],
            "full_name": result["full_name"],
            "email": result["email"],
            "token": token
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/me")
async def get_current_user(token: str = None):
    """Get current user information"""
    if not token or token not in sessions:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    session = sessions[token]
    user = get_user(session["user_id"])
    
    if user:
        return {
            "success": True,
            "user": user
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/logout")
async def logout(token: str = None):
    """Logout user"""
    if token and token in sessions:
        del sessions[token]
    
    return {
        "success": True,
        "message": "Logged out successfully"
    }

@router.post("/check-email")
async def check_email(email: str):
    """Check if email already exists"""
    from database import user_exists
    exists = user_exists(email)
    return {
        "exists": exists,
        "email": email
    }
