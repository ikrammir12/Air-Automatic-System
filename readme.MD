Airport Management System (Air-Automatic-System)
Project Overview

The Airport Management System is a Python-based project that simulates basic operations of an airport flight booking system. The project allows users to:

View all available flights

Book a flight

Cancel a booked flight

All flight and passenger data are stored in a SQLite database, and the system uses Python functions to interact with this database.

Features
1. Flight Database

The project uses a SQLite database (airport.db) to store flight and passenger information. The database contains the following fields:

id: Primary key (integer) for each passenger/booking

name: Name of the passenger (shortened for demonstration purposes)

travelling: Flight route (currently supports Lahore to Karachi)

status: Booking status (Booked or Not Booked)

Sample data in the database:

(101, 'Ali', 'Lahore to Karachi', 'Not Booked')
(102, 'Ahmed', 'Lahore to Karachi', 'Booked')
(103, 'Hassan', 'Lahore to Karachi', 'Not Booked')
2. Functions

The system has the following main Python functions:

view_database()

Fetches and displays all the flight bookings in the database.

Returns all rows as a list of tuples.

Example output:

(101, 'Ali', 'Lahore to Karachi', 'Not Booked')
(102, 'Ahmed', 'Lahore to Karachi', 'Booked')
booked_flight(id)

Updates the status of a passenger to Booked based on their id.

Returns the updated passenger information.

Example usage:

booked_flight(101)
# Output: (101, 'Ali', 'Lahore to Karachi', 'Booked')
cancel_ticket(id)

Updates the status of a passenger to Not Booked based on their id.

Returns the updated passenger information.

Example usage:

cancel_ticket(102)
# Output: (102, 'Ahmed', 'Lahore to Karachi', 'Not Booked')
3. Data Handling

The project uses Python’s sqlite3 module to connect to the database, execute queries, and commit changes:

SELECT for retrieving data

UPDATE for booking and canceling flights

INSERT for adding new records if needed

All database connections are properly closed after each operation to ensure integrity.

4. Tool Integration

The project is designed to integrate with a language model (LLM) assistant:

Tools are defined as Python functions that can be called programmatically.

Tools available:

view_database → View all flight data

booked_flight → Book a ticket

cancel_ticket → Cancel a booked ticket

This allows future integration with AI agents to automate flight management queries.

5. Sample Interaction

View all flights:

view_database()

Output:

(101, 'Ali', 'Lahore to Karachi', 'Not Booked')
(102, 'Ahmed', 'Lahore to Karachi', 'Booked')
(103, 'Hassan', 'Lahore to Karachi', 'Not Booked')

Book a flight:

booked_flight(101)
# Output: (101, 'Ali', 'Lahore to Karachi', 'Booked')

Cancel a flight:

cancel_ticket(102)
# Output: (102, 'Ahmed', 'Lahore to Karachi', 'Not Booked')
6. Technologies Used
3 
Python 3.10+

SQLite for database management

Gradio (optional, for future UI integration)

7. Future Work

Extend to multiple flight routes and airlines

Integrate real-time booking and seat availability

Fully connect AI assistant for automatic flight handling

8. Getting Started

Clone the repository

git clone https://github.com/ikrammir12/Air-Automatic-System.git

Install dependencies (if using Gradio UI)

pip install gradio

Run Python scripts to interact with the database:

python main.py

Use the provided functions to view, book, or cancel flights.



This project aims to build an AI-powered airline booking system where users can interact using natural language to:

Log in using email

Search available flights

Book flights

Cancel bookings

View booking history

The system integrates:

SQLite Database

Python backend logic

LLM tool-calling functionality

Gradio interface (planned integration)