[🏠 Home](../../index.md) > [Management](../index.md)

# ✅ Tasks & Backlog

Оперативный список задач. Глобальный прогресс см. в **[🗺️ Roadmap](../roadmap.md)**.

## 🏃 Active Sprint (Phase 4: Frontend Integration)
Задачи, которые нужно выполнить в первую очередь для связки с фронтендом.

*   [ ] **Auth:** Интеграция JWT на фронтенде (Login/Register формы).
*   [ ] **Media:** Реализация формы загрузки файлов (Drag & Drop).
*   [ ] **Media:** Отображение галереи изображений (Masonry layout).
*   [ ] **Error Handling:** Обработка ошибок API на фронтенде.

## 📋 Backlog (Phase 5: Stabilization)
Задачи по улучшению качества, тесты и CI/CD.

### Documentation & API
*   [ ] [Swagger Error Schemas](./swagger_errors.md) — Описать кастомные схемы ошибок в документации API.
*   [ ] [Secure Swagger UI](./secure_swagger.md) — Скрыть или защитить паролем документацию на проде.

### Security
*   [ ] [Secure Auth Storage (HttpOnly Cookies)](./auth_cookies.md) — Переезд с localStorage на Cookies.

### Testing & Infrastructure
*   [ ] [Backend Testing Strategy](./testing.md) — Написание тестов для Auth и Media.
*   [ ] [CI/CD Pipeline](./ci_cd.md) — Настройка GitHub Actions.

### Code Quality & Refactoring
*   [ ] [Fix Race Condition in Registration](./race_condition_registration.md) — Обработка IntegrityError.
*   [ ] [Refactor User Creation Flags](./user_flags.md) — Убрать хардкод флагов is_active/is_superuser.

---
[🏠 Вернуться на главную](../../index.md)
