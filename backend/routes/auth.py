from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt
from models import UserRegister, UserLogin
from database import get_db

router = APIRouter()

@router.post("/register")
def register(data: UserRegister):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE email=?", (data.email,))
    if c.fetchone():
        conn.close()
        raise HTTPException(400, "Email already registered")
    pw_hash = bcrypt.hash(data.password)
    c.execute("""
        INSERT INTO users (full_name, email, phone, password_hash)
        VALUES (?,?,?,?)
    """, (data.full_name, data.email, data.phone, pw_hash))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return {"message": "Registered successfully", "user_id": user_id, "full_name": data.full_name, "email": data.email}

@router.post("/login")
def login(data: UserLogin):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (data.email,))
    user = c.fetchone()
    conn.close()
    if not user or not bcrypt.verify(data.password, user["password_hash"]):
        raise HTTPException(401, "Invalid email or password")
    return {
        "user_id": user["user_id"],
        "full_name": user["full_name"],
        "email": user["email"]
    }
