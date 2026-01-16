// frontend/js/api.js

class ApiClient {
    constructor() {
        // PROD MODE (Docker + Nginx):
        // Все запросы идут через Nginx (порт 80), который проксирует /api/ на бэкенд.
        // Поэтому baseUrl должен быть относительным или указывать на текущий хост.
        this.baseUrl = '/api/v1';

        this.tokenKey = 'access_token';
    }

    // --- Хелпер для получения полного URL картинки ---
    getImageUrl(path) {
        if (!path) return '';
        if (path.startsWith('http')) return path;

        // Если path уже содержит /api/v1, просто возвращаем его как есть (относительный путь)
        // Браузер сам подставит текущий домен (http://localhost)
        return path;
    }

    // --- Приватный метод для выполнения запросов ---
    async _request(method, endpoint, body = null, isJson = true) {
        const headers = {};

        // 1. Автоматически цепляем токен, если он есть
        const token = localStorage.getItem(this.tokenKey);
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        // 2. Настройка заголовков для тела запроса
        let requestBody = body;

        if (body) {
            if (isJson) {
                headers['Content-Type'] = 'application/json';
                requestBody = JSON.stringify(body);
            }
            // Если отправляем FormData (файлы) или URLSearchParams (логин),
            // браузер сам выставит нужный Content-Type, мы его не трогаем.
        }

        try {
            // ВАЖНО: Убираем порт 8000, если он вдруг где-то проскакивает
            // Запрос должен идти на http://localhost/api/v1/... (порт 80)
            const url = `${this.baseUrl}${endpoint}`;

            const response = await fetch(url, {
                method,
                headers,
                body: requestBody
            });

            // 3. Перехватчик: Если токен протух (401), выкидываем на логин
            if (response.status === 401) {
                console.warn('Unauthorized! Opening login...');
                this.handleUnauthorized();
                // Пытаемся прочитать сообщение об ошибке, если оно есть
                const err = await this._parseError(response);
                throw new Error(err || "Unauthorized");
            }

            // Обработка ошибок API
            if (!response.ok) {
                const errorMessage = await this._parseError(response);
                throw new Error(errorMessage);
            }

            return await response.json();
        } catch (err) {
            console.error(`API Error [${endpoint}]:`, err);
            throw err;
        }
    }

    // --- Хелпер для парсинга ошибок (Smart Error Handling) ---
    async _parseError(response) {
        try {
            const data = await response.json();

            // 1. Наш кастомный формат (backend/core/exceptions.py)
            if (data.error && data.error.message) {
                return data.error.message;
            }

            // 2. Стандартный формат FastAPI (HTTPException)
            if (data.detail) {
                // Если detail - это массив (Validation Error), склеиваем
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

    // --- Публичные методы ---

    // Метод для получения списка (Галерея, Фид)
    async get(endpoint) {
        return this._request('GET', endpoint);
    }

    // Метод для удаления
    async delete(endpoint) {
        return this._request('DELETE', endpoint);
    }

    // --- Специализированные методы (под ваш Backend) ---

    /**
     * Логин под OAuth2PasswordRequestForm (FastAPI)
     * ВАЖНО: Отправляет данные как x-www-form-urlencoded, а не JSON!
     */
    async login(email, password) {
        // FastAPI ожидает поле 'username', даже если мы используем email
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        // false в конце означает "не JSON"
        const data = await this._request('POST', '/auth/login', formData, false);

        // Сохраняем токен
        if (data.access_token) {
            localStorage.setItem(this.tokenKey, data.access_token);
            window.location.reload(); // Обновляем страницу, чтобы показать интерфейс юзера
        }
    }

    /**
     * Регистрация (JSON)
     */
    async register(email, password) {
        return await this._request('POST', '/auth/register', {
            email: email,
            password: password
        });
    }

    /**
     * Загрузка файла
     * ВАЖНО: Отправляет Multipart/form-data
     */
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file); // Имя поля 'file' должно совпадать с аргументом в media.py

        // false означает "не JSON", браузер сам поставит boundary
        return await this._request('POST', '/media/upload', formData, false);
    }

    // --- Утилиты ---

    logout() {
        localStorage.removeItem(this.tokenKey);
        window.location.reload();
    }

    isLoggedIn() {
        return !!localStorage.getItem(this.tokenKey);
    }

    handleUnauthorized() {
        // Пытаемся открыть модалку, если она есть в DOM
        const modal = document.getElementById('login-modal');
        if (modal) {
            // Сбрасываем на логин, если вдруг открыта регистрация
            const viewLogin = document.getElementById('view-login');
            const viewRegister = document.getElementById('view-register');
            if (viewLogin && viewRegister) {
                viewLogin.style.display = 'block';
                viewRegister.style.display = 'none';
            }
            modal.showModal();
        } else {
            // Если модалки нет (редкий кейс), просто алерт
            // alert("Session expired. Please login.");
        }
    }
}

// Экспортируем глобальный инстанс
const api = new ApiClient();