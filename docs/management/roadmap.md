[🏠 Home](../index.md) > [Management](./index.md)

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

## ✅ Phase 3: Media Domain & Storage (Завершено)
Реализация ядра проекта — хостинга изображений.
- [x] **Database Models:** Таблицы `files` (CAS) и `images` (Meta).
- [x] **Storage Logic:**
    - [x] CAS (Content-Addressable Storage) алгоритм.
    - [x] Валидация файлов (Magic bytes / Size limit).
    - [x] Deduplication (проверка хешей).
- [x] **Docker Volumes:** Настройка персистентного хранения (`data/uploads`).
- [x] **API Routers:** Загрузка (`/media/upload`), Галерея (`/media/feed`).
- [x] **Quality Control:** Прохождение проверок `ruff` и `mypy`.

## ✅ Phase 4: Frontend Integration (Завершено)
Связка фронтенда с реальным API.
- [x] **Auth:** Сохранение JWT в localStorage, защита страниц.
- [x] **Upload:** Реальная загрузка файлов на сервер вместо заглушек.
- [x] **Gallery:** Отображение картинок с бэкенда.

## ✅ Phase 5: Stabilization & Testing (Завершено)
Переход к стабильной разработке.
- [x] **Testing:** Написание Unit и Integration тестов (Pytest).
- [x] **Refactoring:** Глобальный аудит кода, внедрение Clean Architecture, Observability (Logs).
- [x] **Documentation:** Обновление README, JSDoc, Docstrings.
- [x] **Infrastructure:** Оптимизация Nginx и Docker.
- [x] **Database Migrations:** Настройка Alembic, автоматические миграции (AUTO_MIGRATE), интеграция в CI/CD.

## 🔮 Phase 6: Future Plans (v2.0)
Планирование следующей версии.
- [ ] **S3 Storage:** Поддержка MinIO/AWS S3.
- [ ] **Image Processing:** Ресайз на лету, водяные знаки.
- [ ] **Admin Panel:** Админка для управления пользователями.
- [ ] **Frontend Framework:** Миграция на Vue.js / React.

---
[🏠 Вернуться на главную](../index.md)
