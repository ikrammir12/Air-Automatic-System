"""
Database Initialization Script
Run this script to initialize the database with sample data
"""

from database import init_db, get_connection
import sys

def main():
    """Initialize database"""
    print("Initializing database...")
    
    try:
        # Initialize database (creates tables and sample data)
        init_db()
        
        # Verify database
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"✅ Users table: {user_count} users")
        
        # Check flights
        cursor.execute("SELECT COUNT(*) FROM flights")
        flight_count = cursor.fetchone()[0]
        print(f"✅ Flights table: {flight_count} flights")
        
        # Check bookings
        cursor.execute("SELECT COUNT(*) FROM bookings")
        booking_count = cursor.fetchone()[0]
        print(f"✅ Bookings table: {booking_count} bookings")
        
        conn.close()
        
        print("\n✅ Database initialized successfully!")
        print("\nTest Credentials:")
        print("  Email: user1@example.com")
        print("  Password: password123")
        print("\nRun 'python main.py' to start the server")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
