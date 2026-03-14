"""
AI Assistant routes
Handles user conversations with the AI assistant
"""

from fastapi import APIRouter, HTTPException
from models import AIMessage, AIResponse
from tools.ai_tools import get_ai_assistant

router = APIRouter()

@router.post("/chat")
async def chat_with_ai(message: AIMessage):
    """Chat with AI assistant"""
    
    if not message.message or not message.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Get AI assistant instance
    ai = get_ai_assistant()
    
    # Check if user is authenticated
    is_authenticated = message.user_id > 0
    
    # Process message
    result = ai.process_message(
        user_id=message.user_id,
        user_message=message.message,
        is_authenticated=is_authenticated
    )
    
    if result["success"]:
        return {
            "success": True,
            "response": result["response"],
            "tool_calls": result.get("tool_calls", []),
            "data": result.get("data", {})
        }
    else:
        raise HTTPException(status_code=500, detail=result["response"])

@router.post("/clear-history")
async def clear_history(user_id: int):
    """Clear conversation history for user"""
    ai = get_ai_assistant()
    ai.clear_history(user_id)
    
    return {
        "success": True,
        "message": "Conversation history cleared"
    }

@router.get("/available-cities")
async def get_available_cities():
    """Get list of available cities"""
    from database import get_connection
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get unique departure and arrival cities
    cursor.execute("""
        SELECT DISTINCT departure_city as city FROM flights
        UNION
        SELECT DISTINCT arrival_city as city FROM flights
        ORDER BY city
    """)
    
    cities = [row["city"] for row in cursor.fetchall()]
    conn.close()
    
    return {
        "success": True,
        "cities": cities
    }
