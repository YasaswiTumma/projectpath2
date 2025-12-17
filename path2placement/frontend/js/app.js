const API_BASE = 'http://localhost:5000/api';

class App {
    constructor() {
        this.token = localStorage.getItem('token');
        this.user = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuth();
    }

    setupEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.id === 'logoutBtn') {
                this.logout();
            }
        });
    }

    checkAuth() {
        if (this.token) {
            this.fetchUserProfile();
            this.showDashboard();
        } else {
            this.showLogin();
        }
    }

    async fetchUserProfile() {
        try {
            const response = await fetch(`${API_BASE}/auth/profile`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
            if (response.ok) {
                this.user = await response.json();
                this.updateHeader();
            } else {
                this.logout();
            }
        } catch (error) {
            console.error('Error fetching profile:', error);
            this.logout();
        }
    }

    updateHeader() {
        document.getElementById('header').classList.remove('d-none');
        document.getElementById('userName').textContent = `Name: ${this.user.name}`;
        document.getElementById('userId').textContent = `ID: ${this.user.student_id || 'N/A'}`;
        document.getElementById('userRole').textContent = `Role: ${this.user.role}`;
    }

    showLogin() {
        this.loadPage('pages/login.html');
    }

    showSignup() {
        this.loadPage('pages/signup.html');
    }

    showDashboard() {
        this.loadPage('pages/dashboard.html');
    }

    async loadPage(page) {
        try {
            const response = await fetch(page);
            const html = await response.text();
            document.getElementById('content').innerHTML = html;
            this.initPage();
        } catch (error) {
            console.error('Error loading page:', error);
        }
    }

    initPage() {
        // Initialize page-specific functionality
        if (document.getElementById('loginForm')) {
            this.initLoginForm();
        } else if (document.getElementById('signupForm')) {
            this.initSignupForm();
        } else if (document.getElementById('dashboard')) {
            this.initDashboard();
        }
    }

    initLoginForm() {
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch(`${API_BASE}/auth/signin`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();
                if (response.ok) {
                    this.token = data.token;
                    localStorage.setItem('token', this.token);
                    this.checkAuth();
                } else {
                    alert(data.message);
                }
            } catch (error) {
                console.error('Login error:', error);
                alert('Login failed');
            }
        });

        document.getElementById('showSignup').addEventListener('click', (e) => {
            e.preventDefault();
            this.showSignup();
        });
    }

    initSignupForm() {
        document.getElementById('signupForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const role = document.getElementById('role').value;
            const studentId = document.getElementById('studentId').value;

            try {
                const response = await fetch(`${API_BASE}/auth/signup`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ name, email, password, role, student_id: studentId })
                });

                const data = await response.json();
                if (response.ok) {
                    alert('Signup successful! Please login.');
                    this.showLogin();
                } else {
                    alert(data.message);
                }
            } catch (error) {
                console.error('Signup error:', error);
                alert('Signup failed');
            }
        });

        document.getElementById('showLogin').addEventListener('click', (e) => {
            e.preventDefault();
            this.showLogin();
        });
    }

    initDashboard() {
        // Initialize dashboard components
        this.renderPRIGauge();
        this.renderLeaderboard();
        this.renderQuickAccessCards();
    }

    renderPRIGauge() {
        // Placeholder for PRI gauge - would integrate with Chart.js or similar
        const priContainer = document.getElementById('priGauge');
        priContainer.innerHTML = `
            <div class="pri-gauge">
                <div class="pri-score">75%</div>
            </div>
            <p class="text-center mt-2">Placement Readiness Index</p>
        `;
    }

    renderLeaderboard() {
        const leaderboard = document.getElementById('leaderboard');
        // Placeholder data
        const mockData = [
            { name: 'Alice Johnson', score: 85, rank: 1 },
            { name: 'Bob Smith', score: 82, rank: 2 },
            { name: 'Charlie Brown', score: 78, rank: 3 },
            { name: 'Diana Prince', score: 75, rank: 4 },
            { name: 'Eve Wilson', score: 72, rank: 5 }
        ];

        leaderboard.innerHTML = mockData.map(item => `
            <div class="leaderboard-item d-flex justify-content-between align-items-center">
                <span><strong>${item.rank}.</strong> ${item.name}</span>
                <span class="badge bg-primary">${item.score}%</span>
            </div>
        `).join('');
    }

    renderQuickAccessCards() {
        const cards = document.querySelectorAll('.quick-access-card');
        cards.forEach(card => {
            card.addEventListener('click', () => {
                const module = card.dataset.module;
                alert(`Navigate to ${module} module`);
                // TODO: Implement navigation to specific modules
            });
        });
    }

    logout() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('token');
        document.getElementById('header').classList.add('d-none');
        this.showLogin();
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new App();
});
