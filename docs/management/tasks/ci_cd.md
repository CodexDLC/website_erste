[🏠 Home](../../index.md) > [Management](../index.md) > [Tasks](./index.md)

# 🚀 Task: CI/CD Pipeline

**Status:** 📋 Backlog
**Priority:** Medium
**Related Tech Debt:** Manual Deploy

## 📝 Описание проблемы
Деплой и проверки качества кода выполняются вручную. Это чревато ошибками ("забыл запустить линтер") и замедляет разработку.

## 🎯 Цель
Автоматизировать проверки и деплой.

## 📋 План реализации

1.  **GitHub Actions (CI):**
    *   Создать workflow `.github/workflows/ci.yml`.
    *   Триггер: Push в `main` и Pull Requests.
    *   Шаги:
        *   Checkout code.
        *   Install dependencies.
        *   Run Linter (`ruff check`).
        *   Run Type Checker (`mypy`).
        *   Run Tests (`pytest`).
2.  **CD (Optional for MVP):**
    *   Автоматическая сборка Docker образа и пуш в Registry.
    *   Деплой на сервер (SSH / Webhook).

---
[⬅️ Вернуться к списку задач](./index.md)
