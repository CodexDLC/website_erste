/**
 * frontend/js/api.js
 * Core API Client for communicating with the Backend.
 * Handles Authentication, Request formatting, and Error parsing.
 */

class ApiClient {
    constructor() {
        // Base URL for API requests.
        // Relative path works because Nginx proxies /api/v1 to the backend.
        this.baseUrl = '/api/v1';
        this.tokenKey = 'access_token';
    }

    /**
     * Helper to resolve full image URL.
     * @param {string} path - Relative path from backend response.
     * @returns {string} - Full URL or relative path.
     */
    getImageUrl(path) {
        if (!path) return '';
        if (path.startsWith('http')) return path;
        return path;
    }

    /**
     * Internal method to execute fetch requests.
     * @param {string} method - HTTP Method (GET, POST, etc.)
     * @param {string} endpoint - API Endpoint (e.g., '/media/feed')
     * @param {object|FormData|URLSearchParams} body - Request payload
     * @param {boolean} isJson - Whether to send as JSON (default: true)
     * @returns {Promise<any>} - JSON response
     * @private
     */
    async _request(method, endpoint, body = null, isJson = true) {
        const headers = {};

        // 1. Attach Authorization header if token exists
        const token = localStorage.getItem(this.tokenKey);
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        // 2. Prepare request body
        let requestBody = body;

        if (body) {
            if (isJson) {
                headers['Content-Type'] = 'application/json';
                requestBody = JSON.stringify(body);
            }
            // For FormData or URLSearchParams, browser sets Content-Type automatically.
        }

        try {
            const url = `${this.baseUrl}${endpoint}`;

            const response = await fetch(url, {
                method,
                headers,
                body: requestBody
            });

            // 3. Handle 401 Unauthorized (Token expired)
            if (response.status === 401) {
                console.warn('API: Unauthorized. Triggering login flow.');
                this.handleUnauthorized();
                const err = await this._parseError(response);
                throw new Error(err || "Unauthorized");
            }

            // 4. Handle other API errors
            if (!response.ok) {
                const errorMessage = await this._parseError(response);
                throw new Error(errorMessage);
            }

            // 5. Handle 204 No Content
            if (response.status === 204) {
                return null;
            }

            // 6. Safe JSON parsing (handles 200 OK with empty body)
            const text = await response.text();
            return text ? JSON.parse(text) : null;

        } catch (err) {
            console.error(`API Error [${endpoint}]:`, err.message);
            throw err;
        }
    }

    /**
     * Parses error response from Backend.
     * Supports standard FastAPI errors and custom BaseAPIException format.
     * @param {Response} response
     * @returns {Promise<string>} - Human-readable error message
     * @private
     */
    async _parseError(response) {
        try {
            const text = await response.text();
            if (!text) return `Error ${response.status}`;

            const data = JSON.parse(text);

            // Custom format (backend/core/exceptions.py)
            if (data.error && data.error.message) {
                return data.error.message;
            }

            // Standard FastAPI format (HTTPException)
            if (data.detail) {
                if (Array.isArray(data.detail)) {
                    return data.detail.map(e => `${e.loc.join('.')}: ${e.msg}`).join('\n');
                }
                return data.detail;
            }

            return `Error ${response.status}`;
        } catch (e) {
            return `Error ${response.status} (Parse failed)`;
        }
    }

    // --- Public Methods ---

    /**
     * Generic GET request.
     * @param {string} endpoint
     */
    async get(endpoint) {
        return this._request('GET', endpoint);
    }

    /**
     * Generic DELETE request.
     * @param {string} endpoint
     */
    async delete(endpoint) {
        return this._request('DELETE', endpoint);
    }

    // --- Domain Specific Methods ---

    /**
     * Authenticate user (OAuth2 Password Flow).
     * Sends data as x-www-form-urlencoded.
     * @param {string} email
     * @param {string} password
     */
    async login(email, password) {
        const formData = new URLSearchParams();
        formData.append('username', email); // FastAPI expects 'username'
        formData.append('password', password);

        const data = await this._request('POST', '/auth/login', formData, false);

        if (data.access_token) {
            localStorage.setItem(this.tokenKey, data.access_token);
            window.location.reload();
        }
    }

    /**
     * Register new user.
     * @param {string} email
     * @param {string} password
     */
    async register(email, password) {
        return await this._request('POST', '/auth/register', {
            email: email,
            password: password
        });
    }

    /**
     * Upload a file (Multipart/form-data).
     * @param {File} file
     */
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        return await this._request('POST', '/media/upload', formData, false);
    }

    // --- Utilities ---

    logout() {
        localStorage.removeItem(this.tokenKey);
        window.location.reload();
    }

    isLoggedIn() {
        return !!localStorage.getItem(this.tokenKey);
    }

    handleUnauthorized() {
        const modal = document.getElementById('login-modal');
        if (modal) {
            const viewLogin = document.getElementById('view-login');
            const viewRegister = document.getElementById('view-register');
            if (viewLogin && viewRegister) {
                viewLogin.style.display = 'block';
                viewRegister.style.display = 'none';
            }
            modal.showModal();
        }
    }
}

// Export global instance
const api = new ApiClient();
