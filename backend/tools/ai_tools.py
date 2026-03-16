"""
AI Integration with Gemini API
Handles AI assistant conversation and tool calling
"""

import os
import json
from typing import Optional, Dict, List
import google.generativeai as genai
from tools.flight_tools import execute_flight_tool
from dotenv import load_dotenv

# Load .env file FIRST
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini API
try:
    genai.configure(api_key=GEMINI_API_KEY)  # ✅ No quotes!
    print("✅ Gemini API configured successfully")
except Exception as e:
    print(f"❌ Gemini API Error: {e}")

# Model name
MODEL_NAME = "gemini-2.5-flash"

class AirlineAI:
    """AI Assistant for Airline Booking System"""
    
    def __init__(self):
        """Initialize AI assistant"""
        try:
            self.model = genai.GenerativeModel(model_name=MODEL_NAME)
            self.conversation_history = {}
            print("✅ AI Assistant initialized")
        except Exception as e:
            print(f"⚠️ AI initialization error: {e}")
            self.model = None
            self.conversation_history = {}
    
    def process_message(self, user_id: int, user_message: str, is_authenticated: bool = False) -> Dict:
        """
        Process user message and generate AI response
        
        Args:
            user_id: The user's ID
            user_message: The user's message
            is_authenticated: Whether user is logged in
            
        Returns:
            Dictionary with AI response and tool calls
        """
        
        # Initialize conversation if needed
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        try:
            # Build system prompt
            if is_authenticated:
                system_prompt = """You are a helpful airline booking assistant.

You help users:
1. Search for flights
2. Book flights
3. View flight details

When user asks about flights, respond naturally but include a JSON block like this:
```json
{
  "action": "search_flights",
  "departure_city": "Lahore",
  "arrival_city": "Karachi",
  "departure_date": "2024-03-20"
}
```

Be helpful and friendly."""
            else:
                system_prompt = """You are a helpful airline assistant.

You help users search for flights.

When user asks about flights, respond naturally and include this JSON:
```json
{
  "action": "search_flights",
  "departure_city": "Lahore",
  "arrival_city": "Karachi"
}
```

Tell users they must login to book flights.

Be helpful and friendly."""
            
            # Build conversation
            # Start with system prompt as first user message
            messages = [
                {"role": "user", "parts": [{"text": system_prompt}]},
            ]
            
            # Add conversation history
            # ✅ FIX: Convert "assistant" to "model" for Google API
            for msg in self.conversation_history[user_id][-10:]:  # Last 10 messages
                role = "model" if msg["role"] == "assistant" else msg["role"]
                messages.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })
            
            # Add current message
            messages.append({
                "role": "user",
                "parts": [{"text": user_message}]
            })
            
            # Call Gemini
            if self.model is None:
                return {
                    "success": False,
                    "response": "AI service is not available. Please try again later.",
                    "tool_calls": [],
                    "data": {}
                }
            
            response = self.model.generate_content(messages)
            response_text = response.text if response.text else "I couldn't process that request."
            
            # Prepare result
            result = {
                "success": True,
                "response": response_text,
                "tool_calls": [],
                "data": {}
            }
            
            # Try to extract and execute JSON action
            try:
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    if json_end > json_start:
                        json_str = response_text[json_start:json_end].strip()
                        action_data = json.loads(json_str)
                        action = action_data.get("action")
                        
                        # Handle search_flights
                        if action == "search_flights":
                            departure = action_data.get("departure_city", "")
                            arrival = action_data.get("arrival_city", "")
                            
                            if departure and arrival:
                                result["tool_calls"].append({
                                    "name": "search_flights",
                                    "input": {
                                        "departure_city": departure,
                                        "arrival_city": arrival,
                                        "departure_date": action_data.get("departure_date")
                                    }
                                })
                                
                                # Execute flight search
                                try:
                                    tool_result = execute_flight_tool(
                                        "search_flights",
                                        {
                                            "departure_city": departure,
                                            "arrival_city": arrival,
                                            "departure_date": action_data.get("departure_date")
                                        }
                                    )
                                    result["data"]["search_flights"] = tool_result
                                except Exception as e:
                                    result["data"]["search_flights"] = {"error": str(e)}
            
            except (json.JSONDecodeError, ValueError, IndexError) as e:
                # JSON parsing failed - just return the text response
                pass
            
            # Add to history
            # ✅ Store as "assistant" in history (will convert to "model" when needed)
            self.conversation_history[user_id].append({
                "role": "user",
                "content": user_message
            })
            self.conversation_history[user_id].append({
                "role": "assistant",
                "content": result["response"]
            })
            
            # Keep history manageable
            if len(self.conversation_history[user_id]) > 20:
                self.conversation_history[user_id] = self.conversation_history[user_id][-20:]
            
            return result
            
        except Exception as e:
            print(f"❌ AI Error: {e}")
            return {
                "success": False,
                "response": f"Sorry, I encountered an error: {str(e)}",
                "error": str(e),
                "tool_calls": [],
                "data": {}
            }
    
    def clear_history(self, user_id: int):
        """Clear conversation history for a user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]

# Global AI instance
ai_assistant = AirlineAI()

def get_ai_assistant() -> AirlineAI:
    """Get the global AI assistant instance"""
    return ai_assistant