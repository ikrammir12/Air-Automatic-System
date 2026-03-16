"""
Airline Booking System - FastAPI Backend
Main application entry point with proper frontend serving
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from contextlib import asynccontextmanager
from pathlib import Path
import os


# Import database and routes
from database import init_db
from routes import auth, flights, bookings, ai

# ========== STARTUP/SHUTDOWN ==========
@asynccontextmanager
async def lifespan(app):
    # Startup
    print("\n" + "="*70)
    print("🚀 AIRLINE BOOKING SYSTEM - STARTING")
    print("="*70)
    
    init_db()
    print("✅ Database initialized")
    
    # Get and display frontend info
    frontend_path = Path(__file__).parent.parent / "frontend"
    print(f"📁 Frontend path: {frontend_path}")
    print(f"✅ Frontend exists: {frontend_path.exists()}")
    
    if frontend_path.exists():
        index_path = frontend_path / "index.html"
        print(f"✅ index.html exists: {index_path.exists()}")
        if index_path.exists():
            file_size = index_path.stat().st_size
            print(f"📄 index.html size: {file_size} bytes")
    
    print("="*70 + "\n")
    
    yield
    
    # Shutdown
    print("\n⬇️ Application shutting down\n")

# ========== FASTAPI APP ==========
app = FastAPI(
    title="Airline Booking System API",
    description="AI-powered airline booking system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# ========== CORS MIDDLEWARE ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== API ROUTES ==========
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(flights.router, prefix="/api/flights", tags=["Flights"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI Assistant"])

# ========== FRONTEND PATH ==========
frontend_path = Path(__file__).parent.parent / "frontend"

# ========== STATIC FILES ==========
# Mount CSS files
css_path = frontend_path / "css"
if css_path.exists():
    app.mount("/css", StaticFiles(directory=str(css_path)), name="css")

# Mount JS files
js_path = frontend_path / "js"
if js_path.exists():
    app.mount("/js", StaticFiles(directory=str(js_path)), name="js")

# Mount assets (images, etc)
assets_path = frontend_path / "assets"
if assets_path.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")

# ========== FRONTEND ROUTES ==========

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve the main index.html file"""
    index_path = frontend_path / "index.html"
    
    if not index_path.exists():
        return """
        <html>
            <body style="font-family: Arial; background: #f0f0f0; padding: 50px;">
                <h1>❌ Frontend Error</h1>
                <p>index.html not found at: """ + str(index_path) + """</p>
                <p>Expected location: """ + str(frontend_path) + """</p>
                <p><a href="/docs">View API Documentation</a></p>
            </body>
        </html>
        """
    
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error reading index.html: {str(e)}</h1>"

# Catch-all for SPA routing (serve index.html for non-API routes)
@app.get("/{path:path}", response_class=HTMLResponse)
async def serve_spa(path: str):
    """Serve index.html for all non-API routes (Single Page App routing)"""
    
    # Don't intercept API, docs, or static file routes
    if path.startswith("api/") or \
       path.startswith("docs") or \
       path.startswith("redoc") or \
       path.startswith("openapi") or \
       path.startswith("css/") or \
       path.startswith("js/") or \
       path.startswith("assets/"):
        raise HTTPException(status_code=404, detail="Not found")
    
    index_path = frontend_path / "index.html"
    
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

# ========== HEALTH CHECK ==========
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "frontend_available": (frontend_path / "index.html").exists()
    }

# ========== ERROR HANDLERS ==========
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return {
        "error": "Not found",
        "path": request.url.path,
        "message": "The requested resource was not found"
    }

# ========== MAIN ==========
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
