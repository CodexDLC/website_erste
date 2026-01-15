[🏠 Home](../../index.md) > [Nginx](index.md)

# ⚙️ Configuration Spec

Ключевые моменты для файла `nginx.conf`.

## 1. Раздача медиа (CAS)
Мы используем директиву `alias`, чтобы Nginx сам отдавал картинки. Бэкенд только генерирует ссылки.

```nginx
location /media/ {
    alias /app/media/;
    expires 30d;  # Кеширование в браузере на месяц
    add_header Cache-Control "public, no-transform";
}
```

## 2. Проксирование API
Необходимо прокидывать реальные IP-адреса клиента, иначе в логах бэкенда везде будет IP докера (внутренний).

```nginx
location /api/ {
    proxy_pass http://backend:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

## 3. SPA / Frontend
Если мы перейдем на React-роутинг (HTML5 History Mode), нам понадобится `try_files`. Пока для Vanilla JS достаточно простой раздачи.

```nginx
location / {
    root /app/frontend;
    index index.html;
    try_files $uri $uri/ /index.html;
}
```

---
[🏠 Вернуться на главную](../../index.md)
