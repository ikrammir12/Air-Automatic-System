const AiAssistant = {
  init() {
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('btn-send');

    sendBtn.addEventListener('click', () => this.send());
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.send();
      }
    });

    document.querySelectorAll('.quick-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        input.value = btn.dataset.msg;
        this.send();
      });
    });

    this.addBotMessage("Hi! I'm SkyBot ✈️ I can help you find and book flights.\n\nTry: \"Show flights from Lahore to Karachi\" or use the quick buttons below!");
  },

  async send() {
    const input = document.getElementById('chat-input');
    const msg = input.value.trim();
    if (!msg) return;

    input.value = '';
    this.addUserMessage(msg);
    this.showTyping();

    try {
      const data = await API.post('/api/ai/chat', {
        message: msg,
        user_id: Auth.user.user_id
      });

      this.removeTyping();

      if (data.book_flight) {
        this.addBotMessage(data.reply);
        await this.bookFlight(data.book_flight);
      } else {
        this.addBotMessage(data.reply);
      }
    } catch(e) {
      this.removeTyping();
      this.addBotMessage('Sorry, something went wrong. Please try again.');
    }
  },

  async bookFlight(flightNumber) {
    try {
      // Find the flight
      const flights = await API.get(`/api/flights/search?from=&to=`);
      const allFlights = await API.get('/api/flights/all');
      const flight = allFlights.find(f => f.flight_number.toUpperCase() === flightNumber.toUpperCase());

      if (!flight) {
        this.addBotMessage(`Sorry, I couldn't find flight ${flightNumber}.`);
        return;
      }

      const result = await API.post('/api/bookings/create', {
        user_id: Auth.user.user_id,
        flight_id: flight.flight_id,
        passenger_name: Auth.user.full_name
      });

      this.addBotMessage(
        `✅ Booking confirmed!\n\n` +
        `Flight: ${result.flight_number}\n` +
        `Seat: ${result.seat_number}\n` +
        `Reference: ${result.booking_reference}\n` +
        `Amount: PKR ${result.price_paid.toLocaleString()}\n\n` +
        `Your booking appears in the dashboard →`
      );

      Toast.show(`Flight ${flightNumber} booked! Ref: ${result.booking_reference}`, 'success');
      await Dashboard.load();
    } catch(e) {
      this.addBotMessage(`Sorry, I couldn't complete the booking: ${e.message}`);
    }
  },

  addUserMessage(text) {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = 'message user';
    div.innerHTML = `
      <div class="msg-avatar">👤</div>
      <div class="msg-bubble">${this.escape(text)}</div>`;
    container.appendChild(div);
    this.scrollToBottom();
  },

  addBotMessage(text) {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = 'message bot';
    div.innerHTML = `
      <div class="msg-avatar">🤖</div>
      <div class="msg-bubble">${this.escape(text)}</div>`;
    container.appendChild(div);
    this.scrollToBottom();
  },

  showTyping() {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = 'message bot';
    div.id = 'typing-indicator';
    div.innerHTML = `
      <div class="msg-avatar">🤖</div>
      <div class="msg-bubble">
        <div class="typing-indicator">
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
        </div>
      </div>`;
    container.appendChild(div);
    this.scrollToBottom();
  },

  removeTyping() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
  },

  scrollToBottom() {
    const c = document.getElementById('chat-messages');
    c.scrollTop = c.scrollHeight;
  },

  escape(text) {
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/\n/g, '<br>');
  }
};
