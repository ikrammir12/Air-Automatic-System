const Dashboard = {
  bookings: [],

  async load() {
    const userId = Auth.user?.user_id;
    if (!userId) return;
    const btn = document.getElementById('btn-refresh');
    if (btn) { btn.innerHTML = '<span class="spin">↻</span> Refreshing...'; btn.disabled = true; }
    try {
      this.bookings = await API.get(`/api/bookings/user/${userId}`);
      this.render();
    } catch(e) {
      Toast.show('Failed to load bookings', 'error');
    } finally {
      if (btn) { btn.innerHTML = '↻ Refresh Bookings'; btn.disabled = false; }
    }
  },

  render() {
    const container = document.getElementById('bookings-container');
    const count = document.getElementById('booking-count');

    if (!this.bookings.length) {
      count.textContent = '0 bookings';
      container.innerHTML = `
        <div class="empty-state">
          <span class="empty-icon">🎫</span>
          <p>No active bookings yet.<br>Ask SkyBot to book a flight!</p>
        </div>`;
      return;
    }

    count.textContent = `${this.bookings.length} booking${this.bookings.length !== 1 ? 's' : ''}`;
    container.innerHTML = this.bookings.map(b => this.cardHTML(b)).join('');

    container.querySelectorAll('.btn-cancel').forEach(btn => {
      btn.addEventListener('click', () => this.cancel(parseInt(btn.dataset.id)));
    });
  },

  cardHTML(b) {
    return `
    <div class="booking-card" id="booking-${b.booking_id}">
      <div class="booking-header">
        <div>
          <div class="booking-flight-num">${b.flight_number}</div>
          <div class="booking-airline">${b.airline}</div>
        </div>
        <span class="badge-booked">● Booked</span>
      </div>
      <div class="booking-route">
        <div>
          <div class="route-city">${b.departure_city}</div>
          <div class="route-time">${b.departure_time}</div>
        </div>
        <div class="route-arrow">
          <div class="route-line"></div>
          ✈
          <div class="route-line"></div>
        </div>
        <div style="text-align:right">
          <div class="route-city">${b.arrival_city}</div>
          <div class="route-time">${b.arrival_time}</div>
        </div>
      </div>
      <div class="booking-details">
        <div class="detail-item">
          <label>Passenger</label>
          <span>${b.passenger_name}</span>
        </div>
        <div class="detail-item">
          <label>Seat</label>
          <span>${b.seat_number}</span>
        </div>
        <div class="detail-item">
          <label>Ref #</label>
          <span>${b.booking_reference}</span>
        </div>
        <div class="detail-item">
          <label>Price</label>
          <span>PKR ${b.price_paid.toLocaleString()}</span>
        </div>
      </div>
      <button class="btn-cancel" data-id="${b.booking_id}">✕ Cancel Booking</button>
    </div>`;
  },

  async cancel(bookingId) {
    if (!confirm('Cancel this booking?')) return;
    const card = document.getElementById(`booking-${bookingId}`);
    if (card) card.style.opacity = '0.5';
    try {
      await API.post(`/api/bookings/cancel/${bookingId}`, {});
      Toast.show('Booking cancelled successfully', 'success');
      await this.load();
    } catch(e) {
      Toast.show('Failed to cancel booking', 'error');
      if (card) card.style.opacity = '1';
    }
  }
};
