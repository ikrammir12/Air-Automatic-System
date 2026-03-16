# ✈️ Airline Booking System - AI-Powered Flight Reservations

An intermediate-level full-stack web application for airline flight booking with AI assistant integration using Google Gemini API.

## 📋 Project Overview

This is a complete airline booking system with the following features:

### Core Features:
1. **User Authentication**
   - Register new users
   - Secure login with session management
   - Logout functionality

2. **Flight Management**
   - Search for flights between cities
   - View flight details (price, departure/arrival times, available seats)
   - Real-time seat availability

3. **Flight Booking**
   - Book single and return flights
   - View all bookings on dashboard
   - Cancel bookings with automatic seat restoration

4. **AI Assistant**
   - Chat-based flight search (e.g., "Lahore to Karachi")
   - AI-powered tool calling for automatic flight operations
   - Context-aware responses

5. **Database**
   - SQLite3 with pre-populated sample data
   - Complete schema for users, flights, bookings, and sessions

## 🏗️ Project Structure

```
airline-booking-system/
│
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # SQLite operations
│   ├── models.py               # Pydantic models
│   ├── requirements.txt        # Python dependencies
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py             # Login/register
│   │   ├── flights.py          # Flight search
│   │   ├── bookings.py         # Booking management
│   │   └── ai.py               # AI assistant
│   └── tools/
│       ├── __init__.py
│       ├── ai_tools.py         # Gemini integration
│       ├── flight_tools.py     # Flight operations
│       └── auth_tools.py       # Auth operations
│
├── frontend/
│   ├── index.html              # Main HTML
│   ├── css/
│   │   ├── style.css           # Main styles
│   │   └── responsive.css      # Mobile responsive
│   └── js/
│       ├── api.js              # API calls
│       ├── auth.js             # Auth logic
│       ├── dashboard.js        # Dashboard logic
│       ├── ai-assistant.js     # AI chat logic
│       └── main.js             # App initialization
│
├── README.md                   # This file
├── .env.example                # Environment variables
└── airline_system.db           # SQLite database (auto-created)
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite3
- **AI Integration**: Google Gemini API (gemini-2.5-flash)
- **API Server**: Uvicorn
- **Validation**: Pydantic

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Flexbox & Grid layouts
- **JavaScript**: Vanilla JS (no frameworks)
- **API Client**: Fetch API

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Google Gemini API Key (Free tier available)
- Modern web browser

### Step 1: Clone or Download the Project

```bash
cd airline-booking-system
```

### Step 2: Set Up Backend

1. **Create Python virtual environment** (optional but recommended):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

2. **Install dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

4. **Get Gemini API Key**:
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Click "Create API Key"
   - Copy the key and paste in `.env` file

### Step 3: Initialize Database

The database is automatically initialized when the server starts, with sample data included.

### Step 4: Run the Backend Server

```bash
cd backend
python main.py
```

The server will start at `http://localhost:8000`

### Step 5: Access the Application

Open your browser and go to:
```
http://localhost:8000
```

The FastAPI server automatically serves the frontend files!

## 🔐 Test Credentials

Use these credentials to test the application:

| Email | Password | Name |
|-------|----------|------|
| user1@example.com | password123 | Ahmed Khan |
| user2@example.com | password123 | Fatima Ali |
| user3@example.com | password123 | Hassan Ibrahim |

You can also create new accounts through the registration form.

## 🚀 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - User logout

### Flights
- `POST /api/flights/search` - Search flights
- `GET /api/flights/{flight_id}` - Get flight details
- `GET /api/flights/` - List all flights

### Bookings
- `POST /api/bookings/create` - Create booking
- `GET /api/bookings/user/{user_id}` - Get user bookings
- `DELETE /api/bookings/{booking_id}` - Cancel booking

### AI Assistant
- `POST /api/ai/chat` - Chat with AI
- `GET /api/ai/available-cities` - Get available cities

### Documentation
- `GET /docs` - Swagger UI (Interactive API docs)
- `GET /redoc` - ReDoc (API documentation)

## 🤖 AI Assistant Usage Examples

Try these commands with the AI assistant:

```
1. "Show me flights from Lahore to Karachi"
   → AI searches and displays all flights

2. "I want to go from Islamabad to Karachi tomorrow"
   → AI searches for specific date

3. "Book flight PK101 for Ahmed Khan"
   → AI books the flight (requires login)

4. "Cancel my last booking"
   → AI helps with cancellation

5. "What cities can I fly to from Lahore?"
   → AI lists available destinations
```

## 💾 Database Schema

### Users Table
```sql
- user_id: Primary key
- email: Unique email
- password: Hashed password
- full_name: User's name
- phone: Phone number
- created_at: Timestamp
- updated_at: Timestamp
```

### Flights Table
```sql
- flight_id: Primary key
- flight_number: Unique identifier
- airline: Airline name
- departure_city: From city
- arrival_city: To city
- departure_time: DateTime
- arrival_time: DateTime
- total_seats: Total capacity
- available_seats: Current available
- price: Flight price
- aircraft_type: Aircraft model
```

### Bookings Table
```sql
- booking_id: Primary key
- user_id: Foreign key to users
- flight_id: Foreign key to flights
- booking_reference: Unique reference code
- passenger_name: Passenger name
- booking_date: DateTime
- status: confirmed/cancelled
- price_paid: Price at booking time
- return_flight_id: Optional return flight
```

## 🎨 UI Features

### Desktop Layout
- **Header**: User info and logout
- **Sidebar**: AI assistant chat (350px width)
- **Main Content**: Dashboard with bookings or search results

### Mobile Responsive
- Sidebar becomes collapsible
- Single column layout
- Touch-friendly buttons
- Optimized for small screens

### Color Scheme
- **Primary**: Blue (#0066cc)
- **Success**: Green (#28a745)
- **Danger**: Red (#dc3545)
- **Light background**: #f8f9fa
- **Text**: #212529

## 🔄 Request/Response Flow

### Flight Search Flow
1. User sends message to AI: "Lahore to Karachi"
2. Frontend calls `/api/ai/chat` with message
3. Backend calls Gemini API with search_flights tool
4. Gemini identifies intent and calls tool
5. Tool executes `search_flights()` from database
6. Results returned to user
7. Frontend displays flight cards with "Book" buttons

### Booking Flow
1. User clicks "Book Flight" on flight card
2. Opens modal with flight details
3. User enters passenger name
4. Optionally selects return flight
5. Frontend calls `/api/bookings/create`
6. Backend books flight and updates seat count
7. Confirmation shown with booking reference
8. Dashboard refreshes to show new booking

### Cancellation Flow
1. User clicks "Cancel Flight" on booking
2. Confirmation dialog appears
3. Frontend calls `/api/bookings/{booking_id}` with DELETE
4. Backend updates booking status and restores seats
5. Dashboard refreshes

## ⚙️ Configuration

### Main.py Settings
```python
# Host and port
uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

# CORS configuration
allow_origins=["*"]  # Change in production
```

### Database Location
```python
DATABASE_PATH = "airline_system.db"  # In backend directory
```

### AI Model
```python
MODEL_NAME = "gemini-2.5-flash"  # Free tier model
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'google.generativeai'"
**Solution**: 
```bash
pip install google-generativeai
```

### Issue: "GEMINI_API_KEY not set"
**Solution**:
1. Get key from https://aistudio.google.com/app/apikey
2. Add to `.env` file: `GEMINI_API_KEY=your_key`

### Issue: "Database is locked"
**Solution**: 
- SQLite uses file locks; close other connections
- Restart the server
- Check for zombie Python processes

### Issue: Frontend not loading
**Solution**:
- Ensure backend is running: `python main.py`
- Check if port 8000 is available
- Clear browser cache (Ctrl+Shift+Del)
- Check console for errors (F12)

### Issue: AI not responding
**Solution**:
- Check Gemini API key is valid
- Verify internet connection
- Check backend logs for errors
- Ensure API key has appropriate permissions

## 📱 Mobile Testing

### Test on Mobile Device
```bash
# Get your computer's IP address
# Windows: ipconfig
# macOS/Linux: ifconfig

# Access from mobile:
http://192.168.x.x:8000
```

### Test in Browser DevTools
- Press F12
- Click device toggle icon (mobile)
- Select device and test

## 🔒 Security Considerations

### Current Implementation
- Passwords hashed with SHA256
- Session tokens stored in localStorage
- CORS enabled (change in production)

### Production Recommendations
1. Use JWT tokens instead of session tokens
2. Implement HTTPS/TLS
3. Use environment variables for sensitive data
4. Implement rate limiting
5. Add input validation on backend
6. Use database password encryption
7. Implement CSRF protection
8. Add user input sanitization

## 📈 Scalability Improvements

1. **Database**: Migrate to PostgreSQL
2. **Caching**: Add Redis for flight searches
3. **API**: Add API versioning
4. **Frontend**: Migrate to React for SPA
5. **Deployment**: Use Docker containers
6. **CI/CD**: Add automated testing

## 🧪 Testing

### Manual Testing Checklist

**Authentication:**
- [ ] Register new user
- [ ] Login with correct credentials
- [ ] Login with wrong password (should fail)
- [ ] Logout successfully

**Flight Search:**
- [ ] Search flights between cities
- [ ] Search with invalid city (should show no results)
- [ ] AI assistant searches correctly

**Booking:**
- [ ] Book single flight
- [ ] Book with return flight
- [ ] Confirm booking reference appears
- [ ] Booking appears in dashboard

**Cancellation:**
- [ ] Cancel booking from dashboard
- [ ] Confirm seats are restored
- [ ] Cancelled booking disappears

## 📚 Learning Outcomes

This project demonstrates:
- ✅ Full-stack web development (frontend + backend)
- ✅ API design with FastAPI
- ✅ Database design with SQLite
- ✅ AI integration with tool calling
- ✅ Responsive UI design
- ✅ Session management
- ✅ Error handling
- ✅ User authentication

## 📝 Sample Flight Data

**Sample flights included:**
- Lahore ↔ Karachi (3 flights each direction)
- Lahore ↔ Islamabad (2 flights each direction)
- Karachi ↔ Islamabad (2 flights each direction)

**Airlines:**
- Pakistan Airlines
- Airblue
- SereneAir

**Price Range:** Rs. 4,200 - Rs. 9,500

## 🎓 Next Steps

1. **Enhance AI**: Add more sophisticated NLP
2. **Add Payments**: Integrate payment gateway
3. **Email Notifications**: Send booking confirmations
4. **Mobile App**: Convert to React Native
5. **Admin Panel**: Add staff management interface
6. **Analytics**: Track popular routes
7. **User Profiles**: Save preferences
8. **Seat Selection**: Visual seat map

## 📞 Support

For issues or questions:
1. Check this README
2. Review console errors (F12)
3. Check backend logs
4. Verify API key and configuration

## 📄 License

This is an educational project. Use freely for learning purposes.

## 👨‍💻 Author

Created as an intermediate-level full-stack project demonstration.

---

**Happy Flying! ✈️**

Last Updated: 2024
