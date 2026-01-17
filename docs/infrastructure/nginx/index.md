[🏠 Home](../../index.md) > [Infrastructure](../index.md)

# 🌐 Nginx Configuration

Мы используем Nginx как Reverse Proxy, Gateway и Web Server для статики.

## 🐳 Docker Image Strategy (New)

PinLite использует отдельный Docker-образ для Nginx:
- **Backend Image:** `ghcr.io/codexdlc/website_erste:latest`
- **Nginx Image:** `ghcr.io/codexdlc/website_erste-nginx:latest`

Конфигурационные файлы (`nginx-main.conf`, `site.conf`) и статика (`frontend/`) **встроены** в Nginx-образ.
Это обеспечивает Immutable Infrastructure и упрощает деплой.

## 📂 Структура конфигурации (Внутри образа)

1.  **`nginx/nginx-main.conf`** -> `/etc/nginx/nginx.conf`
    *   Глобальные настройки (worker_connections, logs).
    *   Gzip сжатие.
    *   Rate Limiting (зоны ограничений).
    *   Подключение конфигов из `conf.d/*.conf`.

2.  **`nginx/site.conf`** -> `/etc/nginx/conf.d/default.conf`
    *   **Server :80** — Редирект на HTTPS + Certbot challenge.
    *   **Server :443** — Основной сайт.
        *   SSL сертификаты.
        *   Security Headers (HSTS, XSS).
        *   Проксирование API на бэкенд.
        *   Раздача статики и медиа.

## 🛡️ Безопасность

*   **SSL/TLS:** Только TLSv1.2 и TLSv1.3. Современные шифры.
*   **HSTS:** Включен (обязательно для .dev доменов).
*   **Rate Limiting:**
    *   API: 10 req/sec (burst 5).
    *   Static: 30 req/sec (burst 20).
*   **WAF Lite:** Блокировка PHP, CGI, SQL-инъекций в URL.

## 🔄 Локальная разработка

Для локального запуска (`docker-compose.yml`) используется упрощенный файл `nginx/nginx.conf`, который содержит всё в одном файле и не требует SSL.

---
[⬅️ Назад к Infrastructure](../index.md)