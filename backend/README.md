# ✈️ AirBook — Airline Booking System

A full-stack airline booking system with an AI-powered chatbot, flight search, and booking management dashboard. Built with FastAPI, SQLite, and vanilla JavaScript.

---

## 📸 Preview

> Split-screen interface: SkyBot AI chat on the left, live bookings dashboard on the right.

---

## 🚀 Features

- **User Authentication** — Register and login with hashed passwords
- **SkyBot AI Assistant** — Natural language flight search and booking via Google Gemini (with smart fallback if no API key)
- **Flight Search** — Search flights by city pair across 14 pre-loaded routes
- **One-Step Booking** — Type "Book PK101" and it's done — seat assigned, reference generated
- **Bookings Dashboard** — Live view of all your active bookings with full details
- **Cancel Booking** — One-click cancellation, seats released back to inventory
- **Responsive UI** — Works on desktop and mobile

---

## 🗂️ Project Structure

```
project/
├── backend/
│   ├── main.py               # FastAPI app entry point, serves frontend
│   ├── database.py           # SQLite connection and table creation
│   ├── models.py             # Pydantic request models
│   ├── init_db.py            # Seeds 14 sample flights and demo user
│   ├── requirements.txt
│   ├── .env                  # Your GEMINI_API_KEY goes here
│   ├── .env.example
│   ├── .gitignore
│   ├── routes/
│   │   ├── auth.py           # /api/auth/register, /api/auth/login
│   │   ├── flights.py        # /api/flights/all, /api/flights/search
│   │   └── bookings.py       # /api/bookings/create, cancel, list
│   └── tools/
│       └── ai_tools.py       # Gemini integration + fallback chatbot
└── frontend/
    ├── index.html
    ├── css/
    │   ├── style.css
    │   └── responsive.css
    └── js/
        ├── api.js            # Fetch wrapper for all API calls
        ├── auth.js           # Login / register logic
        ├── dashboard.js      # Bookings list and cancel
        ├── ai-assistant.js   # Chat UI and booking trigger
        └── main.js           # App initialization and Toast utility
```

---

## ⚙️ Setup & Installation

### 1. Clone / Extract the project

```bash
unzip airbook-system.zip
cd project/backend
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=any_random_secret_string
```

> **Note:** `GEMINI_API_KEY` is optional. If left blank, SkyBot uses a built-in fallback that handles flight search and booking without Gemini.

### 4. Start the server

```bash
python -m uvicorn main:app --reload
```

### 5. Open in browser

```
http://localhost:8000
```

---

## 🔑 Demo Credentials

A demo account is pre-loaded when the database is seeded:

| Field    | Value                  |
|----------|------------------------|
| Email    | `user1@example.com`    |
| Password | `password123`          |

---

## 🗄️ Database Schema

### Users
| Column        | Type    | Notes              |
|---------------|---------|--------------------|
| user_id       | INTEGER | Primary key        |
| full_name     | TEXT    |                    |
| email         | TEXT    | Unique             |
| phone         | TEXT    | Optional           |
| password_hash | TEXT    | bcrypt hashed      |
| created_at    | TIMESTAMP |                  |

### Flights
| Column          | Type    | Notes                        |
|-----------------|---------|------------------------------|
| flight_id       | INTEGER | Primary key                  |
| flight_number   | TEXT    | e.g. PK101                   |
| airline         | TEXT    | e.g. PIA, AirBlue            |
| departure_city  | TEXT    |                              |
| arrival_city    | TEXT    |                              |
| departure_time  | TEXT    | HH:MM format                 |
| arrival_time    | TEXT    | HH:MM format                 |
| price           | INTEGER | In PKR                       |
| total_seats     | INTEGER | Default 50                   |
| available_seats | INTEGER | Decrements on booking        |

### Bookings
| Column            | Type      | Notes                          |
|-------------------|-----------|--------------------------------|
| booking_id        | INTEGER   | Primary key                    |
| user_id           | INTEGER   | Foreign key → users            |
| flight_id         | INTEGER   | Foreign key → flights          |
| passenger_name    | TEXT      |                                |
| seat_number       | TEXT      | Auto-assigned (e.g. 1A, 2B)   |
| booking_reference | TEXT      | Unique (e.g. BK123456)         |
| price_paid        | INTEGER   | PKR at time of booking         |
| booking_date      | TIMESTAMP |                                |
| status            | TEXT      | `booked` or `cancelled`        |

---

## 🛫 Pre-loaded Flights

| Route                    | Flights | Price Range (PKR) |
|--------------------------|---------|-------------------|
| Lahore → Karachi         | 5       | 4,800 – 6,000     |
| Lahore → Islamabad       | 3       | 4,000 – 4,500     |
| Lahore → Peshawar        | 2       | 3,600 – 3,800     |
| Karachi → Islamabad      | 2       | 6,500 – 7,000     |
| Karachi → Peshawar       | 1       | 7,500             |
| Islamabad → Peshawar     | 1       | 3,000             |

**Total: 14 flights**

---

## 🤖 SkyBot — AI Chat Commands

SkyBot understands natural language. Here are example things you can say:

| You say...                             | SkyBot does...                        |
|----------------------------------------|---------------------------------------|
| Show flights from Lahore to Karachi    | Lists all matching flights with times and prices |
| Show all available flights             | Lists all 14 flights                  |
| Book PK101                             | Creates a booking and confirms with reference number |
| Book flight PK301                      | Same as above                         |

> With a valid `GEMINI_API_KEY`, responses are powered by Gemini 1.5 Flash. Without one, the built-in fallback handles all standard requests.

---

## 🌐 API Endpoints

### Authentication
| Method | Endpoint              | Body                                          |
|--------|-----------------------|-----------------------------------------------|
| POST   | `/api/auth/register`  | `{ full_name, email, phone, password }`       |
| POST   | `/api/auth/login`     | `{ email, password }`                         |

### Flights
| Method | Endpoint                           | Params              |
|--------|------------------------------------|---------------------|
| GET    | `/api/flights/all`                 | —                   |
| GET    | `/api/flights/search`              | `?from=X&to=Y`      |

### Bookings
| Method | Endpoint                           | Body / Params                                 |
|--------|------------------------------------|-----------------------------------------------|
| GET    | `/api/bookings/user/{user_id}`     | —                                             |
| POST   | `/api/bookings/create`             | `{ user_id, flight_id, passenger_name }`      |
| POST   | `/api/bookings/cancel/{booking_id}`| —                                             |

### AI Chat
| Method | Endpoint        | Body                          |
|--------|-----------------|-------------------------------|
| POST   | `/api/ai/chat`  | `{ message, user_id }`        |

---

## 🎬 Demo Flow (90 seconds)

```
1. Login          →  user1@example.com / password123
2. Search         →  "Show flights from Lahore to Karachi"
3. Book           →  "Book PK101"
4. Dashboard      →  Booking appears with seat and reference
5. Cancel         →  Click Cancel Booking button
6. Done           →  Dashboard clears, seat back in inventory
```

---

## 🛠️ Tech Stack

| Layer     | Technology               |
|-----------|--------------------------|
| Backend   | Python, FastAPI, Uvicorn |
| Database  | SQLite                   |
| Auth      | bcrypt password hashing  |
| AI        | Google Gemini 1.5 Flash  |
| Frontend  | HTML5, CSS3, Vanilla JS  |
| Fonts     | Sora, JetBrains Mono     |

---

## 📝 Notes

- This is a **demo project** — not production-hardened
- The SQLite database file (`airline.db`) is created automatically on first run
- Passwords are hashed with bcrypt — never stored in plain text
- Sessions are stored in `localStorage` (no JWT expiry for simplicity)
- The frontend is served directly by FastAPI via `StaticFiles`

---

## 📄 License

MIT — free to use, modify, and distribute.
