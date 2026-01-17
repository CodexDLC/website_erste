[🏠 Home](../../index.md) > [Management](../index.md) > [Tasks](./index.md)

# 🐳 Task: Migrate Nginx & Frontend to Docker Image

**Status:** Draft
**Priority:** Medium
**Type:** Infrastructure / DevOps

## 🎯 Цель
Упаковать все конфигурационные файлы (`nginx/`, `frontend/`) в Docker-образы, чтобы VPS получал готовый неизменяемый артефакт без необходимости хранить файлы на хосте.

---

## 🏗️ Архитектура

### Текущая (Вариант 1)
*   **GitHub:** Build Backend Image → Push to GHCR
*   **VPS:** Git pull configs → Mount from host → Run containers

### Целевая (Вариант 2)
*   **GitHub:** Build Backend Image + **Build Nginx Image** → Push to GHCR
*   **VPS:** Pull both images → Run (всё внутри) → **No host files needed**

---

## 📝 ШАГ ЗА ШАГОМ (Detailed Plan)

### ШАГ 1: Создать Dockerfile для Nginx
Файл: `nginx/Dockerfile` (новый)

```dockerfile
# Базовый образ Nginx Alpine (легковесный)
FROM nginx:alpine

# Копируем конфигурационные файлы Nginx
# ВАЖНО: Проверить реальные имена файлов перед копированием!
COPY nginx-main.conf /etc/nginx/nginx.conf
COPY site.conf /etc/nginx/conf.d/default.conf

# Копируем статику Frontend
# Контекст сборки будет в корне репозитория
COPY frontend /usr/share/nginx/html

# Создаём директории для Certbot
RUN mkdir -p /var/www/certbot

# Открываем порты
EXPOSE 80 443

# Запуск Nginx
CMD ["nginx", "-g", "daemon off;"]
```

### ШАГ 2: Обновить docker-compose.prod.yml
Файл: `docker-compose.prod.yml`

Изменить секцию `nginx`:

```yaml
  nginx:
    # === ИЗМЕНЕНО: Используем кастомный образ ===
    image: ${DOCKER_IMAGE_NGINX}
    # ============================================
    container_name: pinlite-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      # === ИЗМЕНЕНО: Убираем монтирование конфигов ===
      # Конфиги теперь ВНУТРИ образа, не нужны с хоста
      # - ./nginx/nginx-main.conf:/etc/nginx/nginx.conf:ro  ← УДАЛЕНО
      # - ./nginx/site.conf:/etc/nginx/conf.d/default.conf:ro ← УДАЛЕНО
      # - ./frontend:/usr/share/nginx/html:ro ← УДАЛЕНО
      # ==============================================
      
      # Оставляем только динамические данные
      - uploads:/app/media:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot:ro
    depends_on:
      backend:
        condition: service_started
    restart: always
    networks:
      - pinlite-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### ШАГ 3: Обновить .env
Добавить переменную для Nginx образа (на VPS и в GitHub Secrets):

```ini
DOCKER_IMAGE_BACKEND=ghcr.io/codexdlc/website_erste:latest
DOCKER_IMAGE_NGINX=ghcr.io/codexdlc/website_erste-nginx:latest
```

### ШАГ 4: Обновить CI/CD Workflow
Файл: `.github/workflows/cd-release.yml`

Добавить сборку Nginx образа:

```yaml
      # === НОВОЕ: Build Nginx Image ===
      - name: Build and Push Nginx Image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./nginx/Dockerfile
          push: true
          tags: ghcr.io/${{ env.REPO_LOWER }}-nginx:latest
      # =================================
```

Обновить SSH скрипт:

```bash
            # Устанавливаем переменные для обоих образов
            export DOCKER_IMAGE_BACKEND=ghcr.io/$REPO_LOWER:latest
            export DOCKER_IMAGE_NGINX=ghcr.io/$REPO_LOWER-nginx:latest
```

### ШАГ 5: Создать .dockerignore
Файл: `nginx/.dockerignore` (новый)

```text
README.md
*.md
.git
.github
```

### ШАГ 6: Обновить документацию
Файл: `docs/infrastructure/nginx/index.md`

Добавить раздел про Docker Image Strategy.

### ШАГ 7-10: Деплой и Верификация
1.  Обновить GitHub Secret `ENV_FILE`.
2.  Сделать коммит и пуш в `release`.
3.  Проверить на VPS:
    *   `docker images | grep website_erste` (должно быть два образа).
    *   `docker exec pinlite-nginx cat /etc/nginx/nginx.conf` (проверить конфиг внутри).
    *   `curl -I https://pinlite.dev` (проверить работу).
4.  (Опционально) Удалить файлы конфигов с хоста `/opt/pinlite/nginx/`.

---

## 📊 Преимущества
*   **Immutability:** Образы неизменяемы, версионируются.
*   **Rollback:** Простой откат (`docker tag previous-version`).
*   **VPS чистота:** Минимум файлов на хосте.
*   **Безопасность:** Нельзя случайно изменить конфиги на VPS.

## 🛟 Troubleshooting
*   **Build не находит ../frontend:** Изменить контекст build в workflow на `.` (корень).
*   **Nginx не видит SSL:** Проверить монтирование `/etc/letsencrypt` (оно должно остаться!).

---
[⬅️ Назад к задачам](./index.md)