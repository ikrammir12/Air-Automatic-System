import sqlite3
conn = sqlite3.connect("airport1.db")
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    name TEXT,
    password TEXT,
    role TEXT
)
""")

# FLIGHTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number TEXT,
    source TEXT,
    destination TEXT,
    date TEXT,
    available_seats INTEGER,
    price INTEGER
)
""")

# BOOKINGS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    flight_id INTEGER,
    status TEXT,
    FOREIGN KEY(user_email) REFERENCES users(email),
    FOREIGN KEY(flight_id) REFERENCES flights(flight_id)
)
""")

# PAYMENTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    amount INTEGER,
    status TEXT,
    FOREIGN KEY(booking_id) REFERENCES bookings(booking_id)
)
""")

conn.commit()

print("Database created successfully")
conn.close()

conn = sqlite3.connect("airport1.db")
cursor = conn.cursor()

# SAMPLE USERS
cursor.execute("INSERT OR IGNORE INTO users VALUES ('user1@gmail.com','Ali','1234','user')")
cursor.execute("INSERT OR IGNORE INTO users VALUES ('admin@gmail.com','Admin','admin123','admin')")

# SAMPLE FLIGHTS
cursor.execute("""
INSERT INTO flights (flight_number,source,destination,date,available_seats,price)
VALUES ('PK101','Karachi','Lahore','2026-03-20',50,200)
""")

cursor.execute("""
INSERT INTO flights (flight_number,source,destination,date,available_seats,price)
VALUES ('PK202','Lahore','Islamabad','2026-03-21',40,150)
""")

conn.commit()
conn.close()

print("Sample data inserted")