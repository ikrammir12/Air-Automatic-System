// Toast utility
const Toast = {
  show(msg, type = 'info') {
    const el = document.createElement('div');
    el.className = `toast ${type}`;
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transition = 'opacity 0.3s';
      setTimeout(() => el.remove(), 300);
    }, 3500);
  }
};

// App controller
const App = {
  showApp() {
    document.getElementById('auth-screen').style.display = 'none';
    const appScreen = document.getElementById('app-screen');
    appScreen.style.display = 'flex';

    // Set user info in topbar
    document.getElementById('topbar-name').textContent = Auth.user.full_name;
    document.getElementById('topbar-email').textContent = Auth.user.email;

    // Load dashboard
    Dashboard.load();
  }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  Auth.init();

  // Refresh button
  document.getElementById('btn-refresh').addEventListener('click', () => Dashboard.load());

  // Check if already logged in
  if (Auth.user) {
    App.showApp();
    AiAssistant.init();
  } else {
    document.getElementById('auth-screen').style.display = 'flex';
    document.getElementById('app-screen').style.display = 'none';
  }

  // Init AI after login
  const origShowApp = App.showApp.bind(App);
  App.showApp = function() {
    origShowApp();
    AiAssistant.init();
  };
});
