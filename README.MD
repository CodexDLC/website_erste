# 📌 PinLite

> 🇬🇧 **English** | [🇷🇺 Русский](#-pinlite-ru)

---

## 🇬🇧 PinLite (EN)

**PinLite** is a modern and lightweight image hosting service.
Designed for developers and content creators who need reliable asset storage with direct links.

> 🚀 **Status:** Active Development (MVP Phase)
> 🌐 **Live Demo:** [https://pinlite.dev](https://pinlite.dev)

### ⚠️ Disclaimer
> **Note:** The full project documentation (Architecture, DevOps, Roadmap) is currently available **in Russian only**. We apologize for the inconvenience.

### ✨ Features
*   **👤 User Dashboard:** Registration and authorization.
*   **📤 Upload:** Drag & Drop interface, format validation, CAS deduplication.
*   **🔗 Direct Links:** Nginx serves files directly (High Performance).
*   **🖼️ Gallery:** Convenient content management.

### 🛠️ Tech Stack
*   **Backend:** FastAPI, SQLAlchemy (Async), PostgreSQL.
*   **Frontend:** Vanilla JS, HTML5, CSS3.
*   **Infra:** Docker Compose, Nginx, GitHub Actions.

### 🚀 Quick Start (Docker)
1.  Create `.env`: `cp .env.example .env`
2.  Run: `docker-compose up -d --build`
3.  Open: `http://localhost`

---

<a name="-pinlite-ru"></a>

## 🇷🇺 PinLite (RU)

**PinLite** — это современный и легковесный сервис хостинга изображений.
Создан для разработчиков и контент-мейкеров, которым нужно надежное хранилище ассетов с прямыми ссылками.

### ✨ Возможности
*   **👤 Личный кабинет:** Регистрация и авторизация пользователей.
*   **📤 Загрузка:** Drag & Drop интерфейс, валидация форматов, дедупликация файлов (CAS).
*   **🔗 Прямые ссылки:** Nginx раздает файлы напрямую (High Performance).
*   **🖼️ Галерея:** Удобный просмотр и управление загруженным контентом.

### 🛠️ Технологический Стек
*   **Backend (Python):** FastAPI, SQLAlchemy (Async), Clean Architecture.
*   **Frontend (Vanilla):** HTML5, CSS3, JavaScript (ES6+).
*   **Infrastructure:** Docker Compose, Nginx, PostgreSQL.

### 📂 Структура Репозитория
*   **[`backend/`](./backend/)** — Серверная часть (API, DB, Logic).
*   **[`frontend/`](./frontend/)** — Клиентская часть (UI/UX).
*   **[`nginx/`](./nginx/)** — Конфигурация веб-сервера.
*   **[`docs/`](./docs/)** — **Полная документация проекта.**
    *   [🏗️ Infrastructure & DevOps](./docs/infrastructure/index.md)
    *   [📅 Management & Roadmap](./docs/management/index.md)

### 🚀 Быстрый Старт (Локально)
Самый простой способ поднять всё окружение (БД, Бэкенд, Nginx).

1.  Создайте файл `.env` (можно скопировать пример):
    ```bash
    cp .env.example .env
    ```
2.  Запустите:
    ```bash
    docker-compose up -d --build
    ```
3.  Откройте: `http://localhost`

---
Developed with ❤️ by [CodexDLC]
