[🏠 Home](../../index.md) > [Management](../index.md)

# ✅ Tasks & Backlog

Оперативный список задач. Глобальный прогресс см. в **[🗺️ Roadmap](../roadmap.md)**.

## 🏃 Active Sprint (Phase 4: Frontend Integration)
Задачи, которые нужно выполнить в первую очередь для связки с фронтендом.

*   [x] **[Frontend API Integration](./frontend_api_integration.md)** — Перевод фронтенда с localStorage на реальный API (Login, Upload, Gallery).

## 🛠️ Infrastructure & DevOps (Phase 5)
*   [x] **[Migrate Nginx to Docker Image](./nginx_docker_migration.md)** — Упаковка конфигов в образ.
*   [ ] **[Backend Optimization](./backend_optimization.md)** — DB Pool, Logging, Async Thumbnails.

## 🎨 Frontend & UX
*   [ ] **[Frontend UX Improvements](./frontend_ux_improvements.md)** — Loading States, Pagination, A11y.

## 🛡️ Security & Privacy
*   [ ] **[Privacy & Security Hardening](./privacy_security.md)** — CORS, EXIF Stripping, Content Moderation.
*   [ ] [Secure Auth Storage (HttpOnly Cookies)](./auth_cookies.md) — Переезд с localStorage на Cookies.

## 📋 Backlog (Tech Debt)
Задачи по улучшению качества кода.

### Documentation & API
*   [x] [Swagger Error Schemas](./swagger_errors.md) — Описать кастомные схемы ошибок в документации API.
*   [x] [Secure Swagger UI](./secure_swagger.md) — Скрыть или защитить паролем документацию на проде.

### Testing
*   [x] [Backend Testing Strategy](./testing.md) — Написание тестов для Auth и Media.

### Code Quality
*   [x] [Fix Race Condition in Registration](./race_condition_registration.md) — Обработка IntegrityError.
*   [ ] [Refactor User Creation Flags](./user_flags.md) — Убрать хардкод флагов is_active/is_superuser.
*   [x] [Critical Fixes (P0)](./critical_fixes.md) — Исправления критических багов.

## 💡 Future Ideas (v2.0)
*   [ ] **[Social Mechanics (Likes)](./social_features.md)** — Лайки и популярное.
*   [ ] **[Headless Mode (Microservice)](./headless_mode.md)** — Режим "Только API" (S3 replacement) по API Key.

---
[🏠 Вернуться на главную](../../index.md)