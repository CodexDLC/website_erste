[🏠 Home](../../index.md) > [Management](../index.md)

# ✅ Tasks & Backlog

Оперативный список задач.
История изменений ведется в **[📜 CHANGELOG.md](../../../CHANGELOG.md)**.

## 🏁 Completed (v1.0 MVP)
Задачи, выполненные в рамках релиза v1.0.

### Infrastructure & DevOps
*   [x] **[CI/CD Pipeline](./ci_cd.md)** — Настройка GitHub Actions (Build, Test, Deploy).
*   [x] **[Migrate Nginx to Docker Image](./nginx_docker_migration.md)** — Упаковка конфигов в образ.
*   [x] **[Backend Optimization](./backend_optimization.md)** — DB Pool (SQLAlchemy), Structured Logging (Loguru).
*   [x] **[Monitoring Setup](./monitoring_setup.md)** — Подготовка логов для Grafana/Loki (JSON/Key-Value).

### Frontend & Integration
*   [x] **[Frontend API Integration](./frontend_api_integration.md)** — Перевод фронтенда с localStorage на реальный API.
*   [x] **[Frontend UX Improvements](./frontend_ux_improvements.md)** — Базовые состояния загрузки, валидация форм.

### Security & Quality
*   [x] [Fix Race Condition in Registration](./race_condition_registration.md) — Обработка IntegrityError.
*   [x] [Critical Fixes (P0)](./critical_fixes.md) — Исправления критических багов.
*   [x] [Backend Testing Strategy](./testing.md) — Unit-тесты для Auth и Media.
*   [x] [Swagger Error Schemas](./swagger_errors.md) — Описание ошибок в документации API.
*   [x] [Secure Swagger UI](./secure_swagger.md) — Отключение Swagger в проде (через DEBUG=False).

## 📋 Backlog (v0.2.0 Candidates)
Задачи, запланированные на следующую версию.

### Security & Privacy
*   [ ] **[Privacy & Security Hardening](./privacy_security.md)** — EXIF Stripping, Content-Security-Policy (CSP) tuning.
*   [ ] [Secure Auth Storage (HttpOnly Cookies)](./auth_cookies.md) — Переезд с localStorage на Cookies (повышение безопасности).

### Features
*   [ ] **[Social Mechanics (Likes)](./social_features.md)** — Лайки и популярное.
*   [ ] **[Headless Mode (Microservice)](./headless_mode.md)** — Режим "Только API" (S3 replacement) по API Key.
*   [ ] [Refactor User Creation Flags](./user_flags.md) — Убрать хардкод флагов is_active/is_superuser (для Админки).

### Frontend
*   [ ] **[Frontend UX Improvements](./frontend_ux_improvements.md)** — Pagination, A11y, Skeleton Loaders.

---
[🏠 Вернуться на главную](../../index.md)
