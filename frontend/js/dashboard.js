/**
 * Dashboard Module
 * Manages user bookings and booking cancellation
 */

let currentBookings = [];
let selectedFlightForBooking = null;
let selectedReturnFlights = [];

// ============= LOAD USER BOOKINGS =============

async function loadUserBookings(userId) {
    const container = document.getElementById("bookings-container");
    container.innerHTML = '<div class="loading">Loading your bookings...</div>';
    
    try {
        const response = await apiGetUserBookings(userId);
        
        if (response.success && response.count > 0) {
            currentBookings = response.bookings;
            displayBookings(response.bookings);
        } else {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>No Bookings Yet</h3>
                    <p>You haven't booked any flights yet.</p>
                    <p>Use the AI Assistant on the left to search and book flights!</p>
                </div>
            `;
        }
    } catch (error) {
        console.error("Error loading bookings:", error);
        container.innerHTML = '<div class="error-message">Error loading bookings</div>';
    }
}

function displayBookings(bookings) {
    const container = document.getElementById("bookings-container");
    container.innerHTML = "";
    
    bookings.forEach(booking => {
        const card = createBookingCard(booking);
        container.appendChild(card);
    });
}

function createBookingCard(booking) {
    const card = document.createElement("div");
    card.className = "booking-card";
    
    const departureTime = new Date(booking.departure_time).toLocaleString();
    const arrivalTime = new Date(booking.arrival_time).toLocaleString();
    
    card.innerHTML = `
        <div class="flight-info">
            <div class="flight-header">
                <div>
                    <div class="flight-number">${booking.flight_number}</div>
                    <div class="airline">${booking.airline}</div>
                </div>
                <div class="status" style="color: #28a745; font-weight: bold;">✓ Confirmed</div>
            </div>
            
            <div class="route">
                <div>
                    <div class="city">${booking.departure_city}</div>
                    <div class="airport-code">From</div>
                </div>
                <div style="text-align: center; flex: 1;">→</div>
                <div style="text-align: right;">
                    <div class="city">${booking.arrival_city}</div>
                    <div class="airport-code">To</div>
                </div>
            </div>
            
            <div class="flight-time">
                <div>
                    <strong>Departure:</strong> ${departureTime}
                </div>
                <div>
                    <strong>Arrival:</strong> ${arrivalTime}
                </div>
            </div>
        </div>
        
        <div class="divider"></div>
        
        <div class="booking-details">
            <p><strong>Booking Reference:</strong> ${booking.booking_reference}</p>
            <p><strong>Passenger:</strong> ${booking.passenger_name}</p>
            <p><strong>Price Paid:</strong> Rs. ${booking.price_paid.toLocaleString()}</p>
            <p><strong>Booked on:</strong> ${new Date(booking.booking_date).toLocaleDateString()}</p>
        </div>
        
        <div class="card-actions">
            <button class="btn btn-danger" onclick="cancelBooking(${booking.booking_id}, '${booking.booking_reference}')">
                Cancel Flight
            </button>
        </div>
    `;
    
    return card;
}

async function cancelBooking(bookingId, reference) {
    if (!confirm(`Are you sure you want to cancel booking ${reference}?`)) {
        return;
    }
    
    try {
        const response = await apiCancelBooking(bookingId);
        
        if (response.success) {
            alert("Booking cancelled successfully!");
            // Reload bookings
            const user = getUser();
            loadUserBookings(user.user_id);
        } else {
            alert("Failed to cancel booking: " + response.message);
        }
    } catch (error) {
        console.error("Error cancelling booking:", error);
        alert("An error occurred while cancelling the booking");
    }
}

function refreshBookings() {
    const user = getUser();
    if (user) {
        loadUserBookings(user.user_id);
    }
}

// ============= FLIGHT SEARCH RESULTS =============

async function displaySearchResults(flights) {
    const container = document.getElementById("flights-container");
    
    if (flights.length === 0) {
        container.innerHTML = `
            <div class="empty-state" style="grid-column: 1 / -1;">
                <h3>No Flights Found</h3>
                <p>Try searching for a different route or date.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = "";
    selectedReturnFlights = [];
    
    flights.forEach(flight => {
        const card = createFlightCard(flight);
        container.appendChild(card);
    });
}

function createFlightCard(flight) {
    const card = document.createElement("div");
    card.className = "flight-card";
    
    const departureTime = new Date(flight.departure_time);
    const arrivalTime = new Date(flight.arrival_time);
    
    const depHours = departureTime.getHours().toString().padStart(2, '0');
    const depMins = departureTime.getMinutes().toString().padStart(2, '0');
    const arrHours = arrivalTime.getHours().toString().padStart(2, '0');
    const arrMins = arrivalTime.getMinutes().toString().padStart(2, '0');
    
    // Calculate duration
    const duration = Math.floor((arrivalTime - departureTime) / (1000 * 60));
    const durationHours = Math.floor(duration / 60);
    const durationMins = duration % 60;
    
    card.innerHTML = `
        <div class="flight-header">
            <div>
                <div class="flight-number">${flight.flight_number}</div>
                <div class="airline">${flight.airline}</div>
            </div>
            <div class="price">Rs. ${flight.price.toLocaleString()}</div>
        </div>
        
        <div class="divider"></div>
        
        <div class="flight-times">
            <div class="time-block">
                <div class="time">${depHours}:${depMins}</div>
                <div class="city-name">${flight.departure_city}</div>
            </div>
            <div class="duration">${durationHours}h ${durationMins}m</div>
            <div class="time-block">
                <div class="time">${arrHours}:${arrMins}</div>
                <div class="city-name">${flight.arrival_city}</div>
            </div>
        </div>
        
        <div class="seats-info">
            <strong>${flight.available_seats}</strong> seats available (out of ${flight.total_seats})
        </div>
        
        <button class="btn btn-primary" onclick="openBookingModal(${flight.flight_id}, '${flight.flight_number}', '${flight.airline}', '${flight.departure_city}', '${flight.arrival_city}', ${flight.price}, '${flight.departure_time}', '${flight.arrival_time}')">
            Book Flight
        </button>
    `;
    
    return card;
}

// ============= BOOKING MODAL =============

let bookingFlightData = null;

function openBookingModal(flightId, flightNumber, airline, depCity, arrCity, price, depTime, arrTime) {
    bookingFlightData = {
        flight_id: flightId,
        flight_number: flightNumber,
        airline: airline,
        departure_city: depCity,
        arrival_city: arrCity,
        price: price,
        departure_time: depTime,
        arrival_time: arrTime
    };
    
    const depDate = new Date(depTime);
    const depFormatted = depDate.toLocaleString();
    const arrDate = new Date(arrTime);
    const arrFormatted = arrDate.toLocaleString();
    
    document.getElementById("modal-flight-details").innerHTML = `
        <div>
            <p><strong>${flightNumber}</strong> (${airline})</p>
            <p>${depCity} → ${arrCity}</p>
            <p><strong>Departure:</strong> ${depFormatted}</p>
            <p><strong>Arrival:</strong> ${arrFormatted}</p>
            <p style="font-size: 18px; color: #28a745;"><strong>Price: Rs. ${price.toLocaleString()}</strong></p>
        </div>
    `;
    
    document.getElementById("passenger-name").value = "";
    document.getElementById("return-flight-checkbox").checked = false;
    document.getElementById("return-flight-select").style.display = "none";
    document.getElementById("booking-error").style.display = "none";
    
    document.getElementById("booking-modal").style.display = "flex";
}

function closeBookingModal() {
    document.getElementById("booking-modal").style.display = "none";
    bookingFlightData = null;
}

document.getElementById("return-flight-checkbox")?.addEventListener("change", function() {
    if (this.checked) {
        // Show return flight select
        document.getElementById("return-flight-select").style.display = "block";
        // Populate with return flights (flights going back from destination)
        populateReturnFlights(bookingFlightData.arrival_city, bookingFlightData.departure_city);
    } else {
        document.getElementById("return-flight-select").style.display = "none";
    }
});

function populateReturnFlights(fromCity, toCity) {
    // This would typically fetch return flights
    // For now, we'll leave it for the user to select manually
    const select = document.getElementById("return-flight-id");
    select.innerHTML = '<option value="">Select return flight...</option>';
}

async function confirmBooking() {
    const passengerName = document.getElementById("passenger-name").value;
    const returnFlightId = document.getElementById("return-flight-checkbox").checked 
        ? document.getElementById("return-flight-id").value 
        : null;
    
    if (!passengerName) {
        const errorDiv = document.getElementById("booking-error");
        errorDiv.textContent = "Please enter passenger name";
        errorDiv.style.display = "block";
        return;
    }
    
    const user = getUser();
    
    try {
        const response = await apiCreateBooking(
            user.user_id,
            bookingFlightData.flight_id,
            passengerName,
            returnFlightId ? parseInt(returnFlightId) : null
        );
        
        if (response.success) {
            alert(`Booking confirmed!\nReference: ${response.booking_reference}`);
            closeBookingModal();
            
            // Reload bookings and close search results
            loadUserBookings(user.user_id);
            closeSearchResults();
        } else {
            const errorDiv = document.getElementById("booking-error");
            errorDiv.textContent = response.message || "Booking failed";
            errorDiv.style.display = "block";
        }
    } catch (error) {
        console.error("Error confirming booking:", error);
        const errorDiv = document.getElementById("booking-error");
        errorDiv.textContent = "An error occurred while booking";
        errorDiv.style.display = "block";
    }
}

function closeSearchResults() {
    document.getElementById("dashboard-section").classList.add("active");
    document.getElementById("search-results-section").classList.remove("active");
}
