[🏠 Home](../../index.md) > [Management](../index.md) > [Tasks](./index.md)

# 📊 Task: Monitoring & Alerting Setup

**Status:** Draft
**Priority:** Medium (P2)
**Type:** DevOps

## 🎯 Цель
Настроить базовый мониторинг доступности сервиса, чтобы узнавать о падениях раньше пользователей.

## 📝 Список задач

### 1. Uptime Monitoring (External)
*   **Инструмент:** UptimeRobot / Better Uptime (Free Tier).
*   **Настройка:**
    *   Ping `https://pinlite.dev/health` каждые 5 минут.
    *   Keyword check: "ok".
    *   Alerts: Email / Telegram.

### 2. Error Tracking (Sentry)
*   **Инструмент:** Sentry (Python SDK).
*   **Настройка:**
    *   Подключить Sentry SDK в `main.py`.
    *   Отправлять Unhandled Exceptions.

---
[⬅️ Назад к задачам](./index.md)