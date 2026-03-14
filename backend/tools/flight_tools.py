"""
Flight search tools for AI assistant
These functions are called by the AI when users ask about flights
"""

from datetime import datetime
from database import search_flights, get_flight, book_flight

# Tool definitions for Gemini
FLIGHT_TOOLS = [
    {
        "name": "search_flights",
        "description": "Search for available flights between two cities on a specific date",
        "parameters": {
            "type": "object",
            "properties": {
                "departure_city": {
                    "type": "string",
                    "description": "City name or code where passenger starts (e.g., 'Lahore', 'LHE')"
                },
                "arrival_city": {
                    "type": "string",
                    "description": "City name or code where passenger lands (e.g., 'Karachi', 'KHI')"
                },
                "departure_date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format (optional, if not provided shows all upcoming flights)"
                }
            },
            "required": ["departure_city", "arrival_city"]
        }
    },
    {
        "name": "get_flight_details",
        "description": "Get detailed information about a specific flight",
        "parameters": {
            "type": "object",
            "properties": {
                "flight_id": {
                    "type": "integer",
                    "description": "The unique flight ID"
                }
            },
            "required": ["flight_id"]
        }
    },
    {
        "name": "book_flight_tool",
        "description": "Book a flight for a passenger",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The user's ID"
                },
                "flight_id": {
                    "type": "integer",
                    "description": "The flight ID to book"
                },
                "passenger_name": {
                    "type": "string",
                    "description": "Full name of the passenger"
                },
                "return_flight_id": {
                    "type": "integer",
                    "description": "Flight ID for return journey (optional)"
                }
            },
            "required": ["user_id", "flight_id", "passenger_name"]
        }
    }
]

def execute_flight_tool(tool_name: str, tool_input: dict) -> dict:
    """Execute flight tool based on tool name"""
    
    if tool_name == "search_flights":
        return execute_search_flights(
            tool_input.get("departure_city"),
            tool_input.get("arrival_city"),
            tool_input.get("departure_date")
        )
    
    elif tool_name == "get_flight_details":
        return execute_get_flight(tool_input.get("flight_id"))
    
    elif tool_name == "book_flight_tool":
        return execute_book_flight(
            tool_input.get("user_id"),
            tool_input.get("flight_id"),
            tool_input.get("passenger_name"),
            tool_input.get("return_flight_id")
        )
    
    return {"error": f"Unknown tool: {tool_name}"}

def execute_search_flights(departure_city: str, arrival_city: str, departure_date: str = None) -> dict:
    """Search for flights"""
    flights = search_flights(departure_city, arrival_city, departure_date)
    
    if flights:
        # Format the response nicely for the AI
        formatted_flights = []
        for flight in flights:
            formatted_flights.append({
                "id": flight["flight_id"],
                "flight_number": flight["flight_number"],
                "airline": flight["airline"],
                "departure": flight["departure_time"],
                "arrival": flight["arrival_time"],
                "available_seats": flight["available_seats"],
                "price": flight["price"]
            })
        
        return {
            "success": True,
            "count": len(formatted_flights),
            "flights": formatted_flights
        }
    else:
        return {
            "success": False,
            "count": 0,
            "flights": [],
            "message": f"No flights found from {departure_city} to {arrival_city}"
        }

def execute_get_flight(flight_id: int) -> dict:
    """Get flight details"""
    flight = get_flight(flight_id)
    
    if flight:
        return {
            "success": True,
            "flight": {
                "id": flight["flight_id"],
                "flight_number": flight["flight_number"],
                "airline": flight["airline"],
                "departure_city": flight["departure_city"],
                "arrival_city": flight["arrival_city"],
                "departure": flight["departure_time"],
                "arrival": flight["arrival_time"],
                "available_seats": flight["available_seats"],
                "total_seats": flight["total_seats"],
                "price": flight["price"]
            }
        }
    else:
        return {
            "success": False,
            "message": f"Flight {flight_id} not found"
        }

def execute_book_flight(user_id: int, flight_id: int, passenger_name: str, return_flight_id: int = None) -> dict:
    """Book a flight"""
    result = book_flight(user_id, flight_id, passenger_name, return_flight_id)
    
    return result
