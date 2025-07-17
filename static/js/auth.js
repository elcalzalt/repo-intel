class AuthManager {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5001/api';  // Your backend API URL
        this.init();
    }

    init() {
        this.bindEvents();
        this.showLogin();
        this.checkExistingSession();
    }

    bindEvents() {
        // Form switching
        document.getElementById('show-signup').addEventListener('click', (e) => {
            e.preventDefault();
            this.showSignup();
        });

        document.getElementById('show-login').addEventListener('click', (e) => {
            e.preventDefault();
            this.showLogin();
        });

        // Form submissions
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        document.getElementById('signupForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSignup();
        });

        // Real-time validation
        document.getElementById('signup-confirm-password').addEventListener('input', (e) => {
            this.validatePasswordMatch();
        });

        document.getElementById('signup-password').addEventListener('input', (e) => {
            this.validatePasswordMatch();
        });

        // Clear error messages on input
        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', (e) => {
                this.clearFieldError(e.target.id);
            });
        });
    }

    showLogin() {
        document.getElementById('login-form').classList.remove('hidden');
        document.getElementById('signup-form').classList.add('hidden');
        this.hideMessage();
        this.clearAllErrors();
    }

    showSignup() {
        document.getElementById('signup-form').classList.remove('hidden');
        document.getElementById('login-form').classList.add('hidden');
        this.hideMessage();
        this.clearAllErrors();
    }

    async handleLogin() {
        const form = document.getElementById('loginForm');
        const formData = new FormData(form);
        const data = {
            username: formData.get('username').trim(),
            password: formData.get('password')
        };

        // Clear previous errors
        this.clearAllErrors();

        // Validate form
        if (!this.validateLoginForm(data)) {
            return;
        }

        const submitButton = document.getElementById('login-btn');
        this.setLoading(submitButton, true);

        try {
            // Using demo mode for testing - switch to apiCall when backend is ready
            const response = await this.simulateApiCall('/auth/login', 'POST', data);
            
            if (response.success) {
                this.showMessage('Login successful! Redirecting...', 'success');
                
                // Store user info in sessionStorage
                sessionStorage.setItem('user', JSON.stringify(response.user));
                sessionStorage.setItem('isLoggedIn', 'true');
                
                // Redirect to profile page after short delay
                setTimeout(() => {
                    window.location.href = 'profile.html';
                }, 1500);
            } else {
                this.showMessage(response.message || 'Login failed. Please check your credentials.', 'error');
            }
        } catch (error) {
            this.showMessage('Connection error. Please try again.', 'error');
            console.error('Login error:', error);
        } finally {
            this.setLoading(submitButton, false);
        }
    }

    async handleSignup() {
        const form = document.getElementById('signupForm');
        const formData = new FormData(form);
        const data = {
            username: formData.get('username').trim(),
            email: formData.get('email').trim(),
            password: formData.get('password'),
            confirmPassword: formData.get('confirmPassword')
        };

        // Clear previous errors
        this.clearAllErrors();

        // Validate form
        if (!this.validateSignupForm(data)) {
            return;
        }

        const submitButton = document.getElementById('signup-btn');
        this.setLoading(submitButton, true);

        try {
            // Using demo mode for testing - switch to apiCall when backend is ready
            const response = await this.simulateApiCall('/auth/signup', 'POST', {
                username: data.username,
                email: data.email,
                password: data.password
            });
            
            if (response.success) {
                this.showMessage('Account created successfully! You can now login.', 'success');
                
                // Clear form and switch to login after delay
                form.reset();
                setTimeout(() => {
                    this.showLogin();
                }, 2000);
            } else {
                this.showMessage(response.message || 'Registration failed. Please try again.', 'error');
            }
        } catch (error) {
            this.showMessage('Connection error. Please try again.', 'error');
            console.error('Signup error:', error);
        } finally {
            this.setLoading(submitButton, false);
        }
    }

    validateLoginForm(data) {
        let isValid = true;

        // Username validation
        if (!data.username) {
            this.showFieldError('login-username', 'Username is required');
            isValid = false;
        } else if (data.username.length < 1 || data.username.length > 50) {
            this.showFieldError('login-username', 'Username must be between 1 and 50 characters');
            isValid = false;
        }

        // Password validation
        if (!data.password) {
            this.showFieldError('login-password', 'Password is required');
            isValid = false;
        }

        return isValid;
    }

    validateSignupForm(data) {
        let isValid = true;

        // Username validation
        if (!data.username) {
            this.showFieldError('signup-username', 'Username is required');
            isValid = false;
        } else if (data.username.length < 1 || data.username.length > 50) {
            this.showFieldError('signup-username', 'Username must be between 1 and 50 characters');
            isValid = false;
        } else if (!/^[a-zA-Z0-9_]+$/.test(data.username)) {
            this.showFieldError('signup-username', 'Username can only contain letters, numbers, and underscores');
            isValid = false;
        }

        // Email validation
        if (!data.email) {
            this.showFieldError('signup-email', 'Email is required');
            isValid = false;
        } else if (data.email.length > 100) {
            this.showFieldError('signup-email', 'Email must be less than 100 characters');
            isValid = false;
        } else if (!this.isValidEmail(data.email)) {
            this.showFieldError('signup-email', 'Please enter a valid email address');
            isValid = false;
        }

        // Password validation
        if (!data.password) {
            this.showFieldError('signup-password', 'Password is required');
            isValid = false;
        } else if (data.password.length < 6) {
            this.showFieldError('signup-password', 'Password must be at least 6 characters');
            isValid = false;
        }

        // Confirm password validation
        if (!data.confirmPassword) {
            this.showFieldError('signup-confirm-password', 'Please confirm your password');
            isValid = false;
        } else if (data.password !== data.confirmPassword) {
            this.showFieldError('signup-confirm-password', 'Passwords do not match');
            isValid = false;
        }

        return isValid;
    }

    validatePasswordMatch() {
        const password = document.getElementById('signup-password').value;
        const confirmPassword = document.getElementById('signup-confirm-password').value;
        
        if (confirmPassword && password !== confirmPassword) {
            this.showFieldError('signup-confirm-password', 'Passwords do not match');
            return false;
        } else if (confirmPassword && password === confirmPassword) {
            this.clearFieldError('signup-confirm-password');
            return true;
        }
        return true;
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    showFieldError(fieldId, message) {
        const field = document.getElementById(fieldId);
        const errorElement = document.getElementById(fieldId + '-error');
        
        if (field && errorElement) {
            field.classList.add('error');
            errorElement.textContent = message;
        }
    }

    clearFieldError(fieldId) {
        const field = document.getElementById(fieldId);
        const errorElement = document.getElementById(fieldId + '-error');
        
        if (field && errorElement) {
            field.classList.remove('error');
            errorElement.textContent = '';
        }
    }

    clearAllErrors() {
        document.querySelectorAll('.error-message').forEach(el => {
            el.textContent = '';
        });
        document.querySelectorAll('input.error').forEach(el => {
            el.classList.remove('error');
        });
    }

    setLoading(button, isLoading) {
        if (isLoading) {
            button.disabled = true;
            button.querySelector('.btn-text').classList.add('hidden');
            button.querySelector('.btn-spinner').classList.remove('hidden');
        } else {
            button.disabled = false;
            button.querySelector('.btn-text').classList.remove('hidden');
            button.querySelector('.btn-spinner').classList.add('hidden');
        }
    }

    showMessage(message, type) {
        const messageContainer = document.getElementById('message-container');
        const messageElement = document.getElementById('message');
        
        messageElement.textContent = message;
        messageContainer.className = `message-container ${type}`;
        messageContainer.classList.remove('hidden');
        
        // Auto-hide success messages after 5 seconds
        if (type === 'success') {
            setTimeout(() => {
                this.hideMessage();
            }, 5000);
        }
    }

    hideMessage() {
        const messageContainer = document.getElementById('message-container');
        messageContainer.classList.add('hidden');
    }

    checkExistingSession() {
        const isLoggedIn = sessionStorage.getItem('isLoggedIn');
        const user = sessionStorage.getItem('user');
        
        if (isLoggedIn && user) {
            this.showMessage('You are already logged in. Redirecting...', 'info');
            setTimeout(() => {
                window.location.href = 'profile.html';
            }, 2000);
        }
    }

    // Simulate API calls - Replace with actual fetch calls when backend is ready
    async simulateApiCall(endpoint, method, data) {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        if (endpoint === '/auth/login') {
            // Simulate login
            if (data.username === 'demo' && data.password === 'password') {
                return {
                    success: true,
                    user: {
                        id: 1,
                        username: 'demo',
                        email: 'demo@example.com'
                    }
                };
            } else {
                return {
                    success: false,
                    message: 'Invalid username or password'
                };
            }
        } else if (endpoint === '/auth/signup') {
            // Simulate signup
            if (data.username === 'demo' || data.email === 'demo@example.com') {
                return {
                    success: false,
                    message: 'Username or email already exists'
                };
            } else {
                return {
                    success: true,
                    message: 'Account created successfully'
                };
            }
        }
    }

    // Method to be called when integrating with real backend
    async apiCall(endpoint, method, data) {
        try {
            console.log(`Making API call to: ${this.apiBaseUrl}${endpoint}`);
            console.log('Request data:', data);
            
            const response = await fetch(`${this.apiBaseUrl}${endpoint}`, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            console.log('Response status:', response.status);
            
            const result = await response.json();
            console.log('Response data:', result);

            if (!response.ok) {
                // Handle HTTP errors with backend message
                throw new Error(result.message || `HTTP error! status: ${response.status}`);
            }

            return result;
        } catch (error) {
            console.error('API call error:', error);
            
            // Check if it's a network error
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                throw new Error('Cannot connect to server. Please make sure the backend is running on http://localhost:5000');
            }
            
            // Re-throw with a user-friendly message
            throw new Error(error.message || 'Connection failed. Please check if the server is running.');
        }
    }
}

// Initialize the AuthManager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AuthManager();
});

// Utility function to get current user from session
function getCurrentUser() {
    const user = sessionStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

// Utility function to check if user is logged in
function isLoggedIn() {
    return sessionStorage.getItem('isLoggedIn') === 'true';
}

// Utility function to logout
function logout() {
    sessionStorage.removeItem('user');
    sessionStorage.removeItem('isLoggedIn');
    window.location.href = 'index.html';
}
