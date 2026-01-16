// js/auth.js
// Управляет логикой авторизации (Login Modal, Register View, Profile Button, Password Toggle, Dropdown)

document.addEventListener('DOMContentLoaded', () => {
    initProfileButton();
    initAuthModalLogic();
    checkAutoLogin();
    initPasswordToggles();

    // Закрытие меню при клике вне его
    document.addEventListener('click', (e) => {
        const dropdown = document.getElementById('profile-dropdown');
        const btn = document.getElementById('profile-btn');
        if (dropdown && dropdown.classList.contains('active')) {
            if (!dropdown.contains(e.target) && !btn.contains(e.target)) {
                dropdown.classList.remove('active');
            }
        }
    });
});

function initPasswordToggles() {
    const toggles = document.querySelectorAll('.toggle-password-btn');
    toggles.forEach(btn => {
        btn.addEventListener('click', () => {
            const input = btn.parentElement.querySelector('input');
            if (!input) return;
            if (input.type === 'password') {
                input.type = 'text';
                btn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>`;
            } else {
                input.type = 'password';
                btn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" y1="2" x2="22" y2="22"/></svg>`;
            }
        });
    });
}

function checkAutoLogin() {
    const params = new URLSearchParams(window.location.search);
    if (params.get('login') === 'true') {
        const modal = document.getElementById('login-modal');
        if (modal && !api.isLoggedIn()) {
            resetModalToLogin();
            modal.showModal();
            window.history.replaceState({}, document.title, window.location.pathname);
        }
    }
}

async function initProfileButton() {
    const btn = document.getElementById('profile-btn');
    const modal = document.getElementById('login-modal');
    const dropdown = document.getElementById('profile-dropdown');
    const emailDisplay = document.getElementById('user-email-display');
    const logoutBtn = document.getElementById('logout-btn');

    if (!btn) return;

    if (api.isLoggedIn()) {
        // ЗАЛОГИНЕН
        btn.classList.add('logged-in');
        btn.title = "Profile";

        // Пытаемся загрузить данные пользователя
        try {
            const user = await api.get('/users/me');
            if (user && user.email) {
                // Рисуем аватарку (Первая буква)
                const letter = user.email.charAt(0).toUpperCase();
                btn.textContent = letter;
                btn.classList.add('avatar-mode');

                // Обновляем email в меню
                if (emailDisplay) emailDisplay.textContent = user.email;
            }
        } catch (err) {
            console.warn("Failed to load user profile:", err);
            // Если токен протух, api.js сам выкинет на логин, так что тут ок
        }

        // Логика клика (Открыть меню)
        btn.onclick = (e) => {
            e.stopPropagation();
            if (dropdown) dropdown.classList.toggle('active');
        };

        // Логика Logout
        if (logoutBtn) {
            logoutBtn.onclick = () => {
                api.logout();
            };
        }

    } else {
        // ГОСТЬ
        btn.classList.remove('logged-in');
        btn.classList.remove('avatar-mode');
        btn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>`;
        btn.title = "Login";

        if (modal) {
            btn.onclick = () => {
                resetModalToLogin();
                modal.showModal();
            };
        }
    }
}

// --- HELPER: SHOW ERROR ---
function showError(formId, message) {
    const errorBlock = document.getElementById(formId + '-error');
    if (errorBlock) {
        // Убираем "Registration failed: " если оно есть, чтобы не дублировать
        const cleanMessage = message.replace("Registration failed: ", "").replace("Login failed: ", "");
        errorBlock.textContent = cleanMessage;
        errorBlock.style.display = 'block';
    } else {
        alert(message);
    }
}

function clearErrors() {
    document.querySelectorAll('.auth-error').forEach(el => {
        el.style.display = 'none';
        el.textContent = '';
    });
}

function initAuthModalLogic() {
    const modal = document.getElementById('login-modal');
    if (!modal) return;

    const viewLogin = document.getElementById('view-login');
    const viewRegister = document.getElementById('view-register');

    const linkToReg = document.getElementById('link-to-register');
    const linkToLog = document.getElementById('link-to-login');

    if (linkToReg) {
        linkToReg.onclick = (e) => {
            e.preventDefault();
            clearErrors();
            viewLogin.style.display = 'none';
            viewRegister.style.display = 'block';
        };
    }

    if (linkToLog) {
        linkToLog.onclick = (e) => {
            e.preventDefault();
            clearErrors();
            viewLogin.style.display = 'block';
            viewRegister.style.display = 'none';
        };
    }

    // --- LOGIN ---
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.onsubmit = async (e) => {
            e.preventDefault();
            clearErrors();

            const btn = loginForm.querySelector('button[type="submit"]');
            const email = loginForm.email.value;
            const password = loginForm.password.value;

            try {
                btn.disabled = true;
                btn.textContent = "Logging in...";
                await api.login(email, password);
            } catch (err) {
                showError('login', err.message);
                btn.disabled = false;
                btn.textContent = "Login";
            }
        };
    }

    // --- REGISTER ---
    const regForm = document.getElementById('register-form');
    if (regForm) {
        regForm.onsubmit = async (e) => {
            e.preventDefault();
            clearErrors();

            const btn = regForm.querySelector('button[type="submit"]');
            const email = regForm.email.value;
            const password = regForm.password.value;
            const confirm = regForm.confirm_password.value;

            if (password !== confirm) {
                showError('register', "Passwords do not match!");
                return;
            }

            try {
                btn.disabled = true;
                btn.textContent = "Creating account...";

                await api.register(email, password);

                alert("Registration successful! Please login.");

                regForm.reset();
                btn.disabled = false;
                btn.textContent = "Sign Up";

                viewRegister.style.display = 'none';
                viewLogin.style.display = 'block';

                if (loginForm) loginForm.email.value = email;

            } catch (err) {
                showError('register', err.message);
                btn.disabled = false;
                btn.textContent = "Sign Up";
            }
        };
    }
}

function resetModalToLogin() {
    clearErrors();
    const viewLogin = document.getElementById('view-login');
    const viewRegister = document.getElementById('view-register');
    if (viewLogin && viewRegister) {
        viewLogin.style.display = 'block';
        viewRegister.style.display = 'none';
    }
}