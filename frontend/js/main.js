/**
 * Main JavaScript File
 * Initializes the application
 */

// Application state
const appState = {
    user: null,
    session: null,
    isLoading: false
};

// Initialize app when DOM is ready
document.addEventListener("DOMContentLoaded", function() {
    initializeApp();
    setupEventListeners();
});

// ============= APP INITIALIZATION =============

function initializeApp() {
    // Check if user is already logged in
    if (isLoggedIn()) {
        const user = getUser();
        appState.user = user;
        appState.session = getSession();
        updateUIAfterLogin(user.full_name);
    } else {
        // Show login form
        document.getElementById("auth-section").style.display = "flex";
        document.getElementById("main-app").style.display = "none";
    }
}

// ============= EVENT LISTENERS =============

function setupEventListeners() {
    // Close modal when clicking outside
    const modal = document.getElementById("booking-modal");
    window.addEventListener("click", function(event) {
        if (event.target === modal) {
            closeBookingModal();
        }
    });
    
    // Handle form submissions
    const loginForm = document.querySelector("#login-form form");
    const registerForm = document.querySelector("#register-form form");
    const chatForm = document.querySelector(".chat-form");
    
    if (loginForm) loginForm.addEventListener("submit", handleLogin);
    if (registerForm) registerForm.addEventListener("submit", handleRegister);
    if (chatForm) chatForm.addEventListener("submit", sendMessage);
}

// ============= KEYBOARD SHORTCUTS =============

document.addEventListener("keydown", function(event) {
    // ESC to close modal
    if (event.key === "Escape") {
        const modal = document.getElementById("booking-modal");
        if (modal && modal.style.display === "flex") {
            closeBookingModal();
        }
    }
});

// ============= UTILITY FUNCTIONS =============

function showLoading(element) {
    element.innerHTML = '<div class="loading">Loading...</div>';
}

function showError(element, message) {
    element.innerHTML = `<div class="error-message">${message}</div>`;
}

function showSuccess(element, message) {
    element.innerHTML = `<div class="success-message">${message}</div>`;
}

// ============= RESPONSIVE HANDLING =============

let screenSize = getScreenSize();

function getScreenSize() {
    return window.innerWidth < 768 ? "mobile" : "desktop";
}

window.addEventListener("resize", function() {
    const newSize = getScreenSize();
    if (newSize !== screenSize) {
        screenSize = newSize;
        handleScreenSizeChange(newSize);
    }
});

function handleScreenSizeChange(size) {
    if (size === "mobile") {
        // Adjust mobile layout if needed
        console.log("Switched to mobile view");
    } else {
        console.log("Switched to desktop view");
    }
}

// ============= ERROR HANDLING =============

window.addEventListener("error", function(event) {
    console.error("Global error:", event.error);
});

window.addEventListener("unhandledrejection", function(event) {
    console.error("Unhandled promise rejection:", event.reason);
});

// ============= PERFORMANCE MONITORING =============

// Log page load time
window.addEventListener("load", function() {
    const perfData = window.performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    console.log("Page load time:", pageLoadTime + "ms");
});
