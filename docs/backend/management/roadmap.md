[🏠 Home](../../index.md) > [Backend](../index.md) > [Management](./index.md)

# 🗺️ Project Roadmap: PinLite

План разработки MVP (Minimum Viable Product) и дальнейшего развития.

## ✅ Phase 1: Foundation (Завершено)
Создание фундамента приложения.
- [x] **Monorepo Structure:** Настройка папок backend/frontend, docs.
- [x] **Core Layer:** Config, Database (Async Engine), Logger (Loguru), Security.
- [x] **Environment:** Docker setup, .env, requirements.
- [x] **Documentation:** Базовая структура документации.

## ✅ Phase 2: Users Domain (Завершено)
Реализация системы пользователей и авторизации.
- [x] **Database Models:** Таблица `users` (SQLAlchemy).
- [x] **Schemas:** Pydantic модели (UserCreate, UserLogin, UserResponse).
- [x] **Repositories:** CRUD операции для пользователей.
- [x] **Services:**
    - [x] Registration (Hashing password).
    - [x] Authentication (JWT Token generation).
- [x] **API Routers:** Эндпоинты `/auth/register`, `/auth/login`, `/users/me`.
- [x] **Quality Control:** Прохождение проверок `ruff` и `mypy` (Basic checks passed).

## 🚧 Phase 3: Media Domain & Storage (В работе)
Реализация ядра проекта — хостинга изображений.
- [ ] **Database Models:** Таблицы `files` (CAS) и `images` (Meta).
- [ ] **Storage Logic:**
    - [ ] CAS (Content-Addressable Storage) алгоритм.
    - [ ] Валидация файлов (Magic bytes).
- [ ] **Docker Volumes:** Настройка персистентного хранения (`data/uploads`).
- [ ] **API Routers:** Загрузка (`/media/upload`), Галерея (`/media/feed`).
- [ ] **Quality Control:** Прохождение проверок `ruff` и `mypy`.

## 📅 Phase 4: Frontend Integration (MVP Release)
Связка фронтенда с реальным API.
- [ ] **Auth:** Сохранение JWT в localStorage, защита страниц.
- [ ] **Upload:** Реальная загрузка файлов на сервер вместо заглушек.
- [ ] **Gallery:** Отображение картинок с бэкенда.

## 🔮 Phase 5: Stabilization & Testing (Post-MVP)
Переход к стабильной разработке.
- [ ] **Testing:** Написание Unit и Integration тестов (Pytest).
- [ ] **Refactoring:** Оптимизация кода на основе тестов.
- [ ] **New Roadmap:** Планирование версии v2.0 (RPG Integration, S3, etc.).

---
[🏠 Вернуться на главную](../../index.md)
