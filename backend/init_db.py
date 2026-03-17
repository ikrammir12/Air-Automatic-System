from database import get_db, init_tables
from passlib.hash import bcrypt

def seed():
    init_tables()
    conn = get_db()
    c = conn.cursor()

    # Check if already seeded
    c.execute("SELECT COUNT(*) FROM flights")
    if c.fetchone()[0] > 0:
        print("Database already seeded.")
        conn.close()
        return

    # Sample flights
    flights = [
        # Lahore -> Karachi (5)
        ("PK101", "PIA",       "Lahore",    "Karachi",    "10:00", "11:30", 5000, 50, 45),
        ("PK102", "PIA",       "Lahore",    "Karachi",    "14:00", "15:30", 5500, 50, 42),
        ("PK103", "PIA",       "Lahore",    "Karachi",    "18:00", "19:30", 4800, 50, 48),
        ("PA201", "AirBlue",   "Lahore",    "Karachi",    "08:00", "09:30", 6000, 50, 30),
        ("PA202", "AirBlue",   "Lahore",    "Karachi",    "21:00", "22:30", 5200, 50, 40),
        # Lahore -> Islamabad (3)
        ("PK301", "PIA",       "Lahore",    "Islamabad",  "08:00", "09:00", 4500, 50, 35),
        ("PK302", "PIA",       "Lahore",    "Islamabad",  "13:00", "14:00", 4000, 50, 44),
        ("PA301", "AirBlue",   "Lahore",    "Islamabad",  "17:00", "18:00", 4200, 50, 38),
        # Lahore -> Peshawar (2)
        ("PK401", "PIA",       "Lahore",    "Peshawar",   "09:00", "10:10", 3800, 50, 46),
        ("PK402", "PIA",       "Lahore",    "Peshawar",   "16:00", "17:10", 3600, 50, 42),
        # Karachi -> Islamabad (2)
        ("PK501", "PIA",       "Karachi",   "Islamabad",  "11:00", "12:30", 6500, 50, 28),
        ("PA501", "AirBlue",   "Karachi",   "Islamabad",  "15:00", "16:30", 7000, 50, 22),
        # Karachi -> Peshawar (1)
        ("PK601", "PIA",       "Karachi",   "Peshawar",   "07:00", "09:00", 7500, 50, 33),
        # Islamabad -> Peshawar (1)
        ("PK701", "PIA",       "Islamabad", "Peshawar",   "12:00", "12:45", 3000, 50, 47),
    ]

    c.executemany("""
        INSERT INTO flights (flight_number, airline, departure_city, arrival_city,
            departure_time, arrival_time, price, total_seats, available_seats)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, flights)

    # Demo user
    pw_hash = bcrypt.hash("password123")
    c.execute("""
        INSERT OR IGNORE INTO users (full_name, email, phone, password_hash)
        VALUES (?, ?, ?, ?)
    """, ("Demo User", "user1@example.com", "03001234567", pw_hash))

    conn.commit()
    conn.close()
    print("✅ Database seeded with 14 flights and demo user.")

if __name__ == "__main__":
    seed()
