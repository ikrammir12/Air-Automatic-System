/**
 * AI Assistant Module - WITH DASHBOARD REFRESH
 * Simplified version + proper dashboard update
 */

let currentConversation = [];

// ============= SEND MESSAGE TO AI =============

async function sendMessage(event) {
    event.preventDefault();
    
    const input = document.getElementById("chat-input");
    const message = input.value.trim();
    
    if (!message) return;
    
    input.value = "";
    addMessageToChat(message, "user");
    
    currentConversation.push({ role: "user", content: message });
    
    const user = getUser();
    const userId = user ? user.user_id : 0;
    
    try {
        const response = await apiChatWithAI(userId, message);
        
        if (response.success) {
            addMessageToChat(response.response, "assistant");
            
            // ✅ IMPORTANT: Always refresh dashboard after message
            if (userId > 0) {
                console.log("📊 Refreshing dashboard after message...");
                
                // Wait for backend to process
                setTimeout(() => {
                    console.log("⏳ Loading bookings...");
                    loadUserBookings(userId);
                }, 1500);
            }
        } else {
            addMessageToChat(response.response || "Sorry, I encountered an error.", "assistant");
        }
    } catch (error) {
        console.error("Chat error:", error);
        addMessageToChat("Sorry, I'm having trouble connecting. Please try again.", "assistant");
    }
}

function addMessageToChat(message, sender) {
    const messagesDiv = document.getElementById("chat-messages");
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message`;
    messageDiv.style.backgroundColor = sender === "user" ? "#007bff" : "#e9ecef";
    messageDiv.style.color = sender === "user" ? "white" : "black";
    messageDiv.style.padding = "12px 15px";
    messageDiv.style.margin = "8px 0";
    messageDiv.style.borderRadius = "8px";
    messageDiv.style.maxWidth = "90%";
    messageDiv.style.wordWrap = "break-word";
    messageDiv.innerHTML = `<p style="margin: 0; white-space: pre-wrap; color: inherit;">${escapeHtml(message)}</p>`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// ============= INITIALIZE =============

document.addEventListener("DOMContentLoaded", function() {
    const chatInput = document.getElementById("chat-input");
    if (chatInput) {
        chatInput.focus();
    }
});
