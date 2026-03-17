const Auth = {
  user: null,

  init() {
    const stored = localStorage.getItem('airbook_user');
    if (stored) {
      try { this.user = JSON.parse(stored); } catch(e) {}
    }

    document.getElementById('tab-login').addEventListener('click', () => this.showTab('login'));
    document.getElementById('tab-register').addEventListener('click', () => this.showTab('register'));
    document.getElementById('login-form').addEventListener('submit', (e) => { e.preventDefault(); this.login(); });
    document.getElementById('register-form').addEventListener('submit', (e) => { e.preventDefault(); this.register(); });
    document.getElementById('btn-logout').addEventListener('click', () => this.logout());
  },

  showTab(tab) {
    document.getElementById('tab-login').classList.toggle('active', tab === 'login');
    document.getElementById('tab-register').classList.toggle('active', tab === 'register');
    document.getElementById('login-form').style.display = tab === 'login' ? 'block' : 'none';
    document.getElementById('register-form').style.display = tab === 'register' ? 'block' : 'none';
    document.getElementById('auth-error').style.display = 'none';
  },

  async login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const btn = document.getElementById('btn-login');
    btn.textContent = 'Signing in...';
    btn.disabled = true;
    try {
      const data = await API.post('/api/auth/login', { email, password });
      this.setUser(data);
      App.showApp();
    } catch(e) {
      this.showError(e.message);
    } finally {
      btn.textContent = 'Sign In';
      btn.disabled = false;
    }
  },

  async register() {
    const full_name = document.getElementById('reg-name').value;
    const email = document.getElementById('reg-email').value;
    const phone = document.getElementById('reg-phone').value;
    const password = document.getElementById('reg-password').value;
    const btn = document.getElementById('btn-register');
    btn.textContent = 'Creating account...';
    btn.disabled = true;
    try {
      const data = await API.post('/api/auth/register', { full_name, email, phone, password });
      this.setUser(data);
      App.showApp();
      Toast.show('Account created! Welcome aboard! ✈️', 'success');
    } catch(e) {
      this.showError(e.message);
    } finally {
      btn.textContent = 'Create Account';
      btn.disabled = false;
    }
  },

  setUser(data) {
    this.user = data;
    localStorage.setItem('airbook_user', JSON.stringify(data));
  },

  logout() {
    this.user = null;
    localStorage.removeItem('airbook_user');
    document.getElementById('app-screen').style.display = 'none';
    document.getElementById('auth-screen').style.display = 'flex';
  },

  showError(msg) {
    const el = document.getElementById('auth-error');
    el.textContent = msg;
    el.style.display = 'block';
  }
};
