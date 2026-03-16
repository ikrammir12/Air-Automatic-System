/**
 * API Communication Module
 * Handles all backend API calls
 */

const API_BASE_URL = "http://localhost:8000/api";

// ============= AUTHENTICATION API =============

async function apiRegister(email, password, fullName, phone) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email,
                password,
                full_name: fullName,
                phone
            })
        });
        return await response.json();
    } catch (error) {
        console.error("Register API error:", error);
        return { success: false, message: "Network error" };
    }
}

async function apiLogin(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        return await response.json();
    } catch (error) {
        console.error("Login API error:", error);
        return { success: false, message: "Network error" };
    }
}

async function apiGetCurrentUser(token) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/me?token=${token}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });
        return await response.json();
    } catch (error) {
        console.error("Get user API error:", error);
        return { success: false, message: "Network error" };
    }
}

async function apiLogout(token) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/logout?token=${token}`, {
            method: "POST"
        });
        return await response.json();
    } catch (error) {
        console.error("Logout API error:", error);
        return { success: false };
    }
}

// ============= FLIGHTS API =============

async function apiSearchFlights(departure, arrival, date) {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/search`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                departure_city: departure,
                arrival_city: arrival,
                departure_date: date
            })
        });
        return await response.json();
    } catch (error) {
        console.error("Search flights API error:", error);
        return { success: false, flights: [] };
    }
}

async function apiGetFlight(flightId) {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/${flightId}`);
        return await response.json();
    } catch (error) {
        console.error("Get flight API error:", error);
        return { success: false };
    }
}

async function apiListAllFlights() {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/`);
        return await response.json();
    } catch (error) {
        console.error("List flights API error:", error);
        return { success: false, flights: [] };
    }
}

// ============= BOOKINGS API =============

async function apiCreateBooking(userId, flightId, passengerName, returnFlightId = null) {
    try {
        const response = await fetch(`${API_BASE_URL}/bookings/create?user_id=${userId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                flight_id: flightId,
                passenger_name: passengerName,
                return_flight_id: returnFlightId
            })
        });
        return await response.json();
    } catch (error) {
        console.error("Create booking API error:", error);
        return { success: false, message: "Network error" };
    }
}

async function apiGetUserBookings(userId) {
    try {
        const response = await fetch(`${API_BASE_URL}/bookings/user/${userId}`);
        return await response.json();
    } catch (error) {
        console.error("Get bookings API error:", error);
        return { success: false, bookings: [] };
    }
}

async function apiCancelBooking(bookingId) {
    try {
        const response = await fetch(`${API_BASE_URL}/bookings/${bookingId}`, {
            method: "DELETE"
        });
        return await response.json();
    } catch (error) {
        console.error("Cancel booking API error:", error);
        return { success: false, message: "Network error" };
    }
}

// ============= AI ASSISTANT API =============

async function apiChatWithAI(userId, message) {
    try {
        const response = await fetch(`${API_BASE_URL}/ai/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: userId,
                message: message
            })
        });
        return await response.json();
    } catch (error) {
        console.error("AI chat API error:", error);
        return { 
            success: false, 
            response: "Sorry, I'm having trouble connecting. Please try again." 
        };
    }
}

async function apiGetAvailableCities() {
    try {
        const response = await fetch(`${API_BASE_URL}/ai/available-cities`);
        return await response.json();
    } catch (error) {
        console.error("Get cities API error:", error);
        return { success: false, cities: [] };
    }
}
