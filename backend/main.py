from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from database import init_tables
from init_db import seed
from routes import auth, flights, bookings
from tools.ai_tools import chat
from models import ChatMessage

app = FastAPI(title="AirBook - Airline Booking System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Init DB on startup
init_tables()
seed()

# Routers
app.include_router(auth.router, prefix="/api/auth")
app.include_router(flights.router, prefix="/api/flights")
app.include_router(bookings.router, prefix="/api/bookings")

@app.post("/api/ai/chat")
async def ai_chat(data: ChatMessage):
    result = await chat(data.message, data.user_id)
    return result

# Serve frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/{full_path:path}")
def serve_frontend(full_path: str):
    path = os.path.join(FRONTEND_DIR, full_path)
    if os.path.isfile(path):
        return FileResponse(path)
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
