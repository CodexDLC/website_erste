[🏠 Home](../../index.md) > [Management](../index.md) > [Tasks](./index.md)

# 🛡️ Task: Privacy & Security Hardening

**Status:** Draft
**Priority:** Medium (P2)
**Type:** Security

## 🎯 Цель
Устранить потенциальные уязвимости и улучшить приватность пользователей.

## 📝 Список задач

### 1. CORS Configuration Check
*   **Проблема:** Риск неправильной настройки `ALLOWED_ORIGINS` на проде. Если там `*` или `localhost`, это дыра.
*   **Решение:**
    *   Проверить `.env` на сервере.
    *   Убедиться, что `allow_origin_regex` выключен в проде.
*   **Действие (Verification):**
    1.  SSH на VPS.
    2.  `cat /opt/pinlite/.env | grep ALLOWED_ORIGINS`
    3.  Должно быть: `ALLOWED_ORIGINS=["https://pinlite.dev"]`

### 2. HTTP Security Headers (CSP)
*   **Проблема:** Отсутствует Content-Security-Policy (CSP), что делает сайт уязвимым к XSS.
*   **Решение:**
    *   Добавить в Nginx:
        ```nginx
        add_header Content-Security-Policy "default-src 'self'; img-src 'self' data:; script-src 'self' 'unsafe-inline';" always;
        add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
        ```

### 3. EXIF Data Stripping
*   **Проблема:** Фото с телефона содержат GPS координаты.
*   **Решение:**
    *   Удалять EXIF метаданные при сохранении файла (используя Pillow).
    *   Оставлять только Orientation (чтобы фото не перевернулось).

### 4. Content Moderation (Future)
*   **Проблема:** Нет защиты от запрещенного контента.
*   **Решение:**
    *   Интеграция с AI сервисами модерации (AWS Rekognition, Google Vision).
    *   Система жалоб (Report).

---
[⬅️ Назад к задачам](./index.md)