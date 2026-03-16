/**
 * Authentication Module
 * Handles user login, registration, and session management
 */

// Session storage keys
const SESSION_KEY = "airline_session";
const USER_KEY = "airline_user";

// ============= FORM SWITCHING =============

function switchForm(formName) {
    document.getElementById("login-form").classList.remove("active");
    document.getElementById("register-form").classList.remove("active");
    document.getElementById(`${formName}-form`).classList.add("active");
    
    // Clear errors
    document.getElementById("login-error").style.display = "none";
    document.getElementById("register-error").style.display = "none";
}

// ============= REGISTRATION =============

async function handleRegister(event) {
    event.preventDefault();
    
    const name = document.getElementById("register-name").value;
    const email = document.getElementById("register-email").value;
    const phone = document.getElementById("register-phone").value;
    const password = document.getElementById("register-password").value;
    const confirm = document.getElementById("register-confirm").value;
    const errorDiv = document.getElementById("register-error");
    
    // Validation
    if (password !== confirm) {
        errorDiv.textContent = "Passwords do not match";
        errorDiv.style.display = "block";
        return;
    }
    
    if (password.length < 6) {
        errorDiv.textContent = "Password must be at least 6 characters";
        errorDiv.style.display = "block";
        return;
    }
    
    try {
        const response = await apiRegister(email, password, name, phone);
        
        if (response.success) {
            // Show success message and switch to login
            alert("Registration successful! Please login.");
            switchForm("login");
            
            // Clear form
            document.getElementById("register-name").value = "";
            document.getElementById("register-email").value = "";
            document.getElementById("register-phone").value = "";
            document.getElementById("register-password").value = "";
            document.getElementById("register-confirm").value = "";
            
        } else {
            errorDiv.textContent = response.message || "Registration failed";
            errorDiv.style.display = "block";
        }
    } catch (error) {
        errorDiv.textContent = "An error occurred. Please try again.";
        errorDiv.style.display = "block";
    }
}

// ============= LOGIN =============

async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;
    const errorDiv = document.getElementById("login-error");
    
    try {
        const response = await apiLogin(email, password);
        
        if (response.success) {
            // Save session
            const session = {
                token: response.token,
                user_id: response.user_id,
                email: response.email,
                full_name: response.full_name,
                login_time: new Date().toISOString()
            };
            
            localStorage.setItem(SESSION_KEY, JSON.stringify(session));
            localStorage.setItem(USER_KEY, JSON.stringify({
                user_id: response.user_id,
                email: response.email,
                full_name: response.full_name
            }));
            
            // Update UI
            updateUIAfterLogin(response.full_name);
            
            // Clear form
            document.getElementById("login-email").value = "";
            document.getElementById("login-password").value = "";
            
        } else {
            errorDiv.textContent = response.message || "Login failed";
            errorDiv.style.display = "block";
        }
    } catch (error) {
        errorDiv.textContent = "An error occurred. Please try again.";
        errorDiv.style.display = "block";
    }
}

// ============= LOGOUT =============

async function handleLogout() {
    const session = getSession();
    
    if (session && session.token) {
        try {
            await apiLogout(session.token);
        } catch (error) {
            console.error("Logout error:", error);
        }
    }
    
    // Clear session
    localStorage.removeItem(SESSION_KEY);
    localStorage.removeItem(USER_KEY);
    
    // Update UI
    updateUIAfterLogout();
}

// ============= SESSION MANAGEMENT =============

function getSession() {
    const session = localStorage.getItem(SESSION_KEY);
    return session ? JSON.parse(session) : null;
}

function getUser() {
    const user = localStorage.getItem(USER_KEY);
    return user ? JSON.parse(user) : null;
}

function isLoggedIn() {
    return getSession() !== null;
}

// ============= UI UPDATES =============

function updateUIAfterLogin(fullName) {
    // Hide auth section, show main app
    document.getElementById("auth-section").style.display = "none";
    document.getElementById("main-app").style.display = "flex";
    
    // Update user name in header
    document.getElementById("user-name").textContent = `Welcome, ${fullName}!`;
    
    // Load user bookings
    const user = getUser();
    if (user) {
        loadUserBookings(user.user_id);
    }
}

function updateUIAfterLogout() {
    // Show auth section, hide main app
    document.getElementById("auth-section").style.display = "flex";
    document.getElementById("main-app").style.display = "none";
    
    // Show login form
    switchForm("login");
    
    // Clear any open modals
    document.getElementById("booking-modal").style.display = "none";
}

// ============= INITIALIZATION =============

document.addEventListener("DOMContentLoaded", function() {
    if (isLoggedIn()) {
        const user = getUser();
        updateUIAfterLogin(user.full_name);
    }
});
