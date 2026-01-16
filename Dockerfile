# === STAGE 1: Builder ===
FROM python:3.12-slim AS builder

WORKDIR /app

# Системные зависимости для сборки
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libmagic1 \
    libmagic-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаём виртуальное окружение
RUN python -m venv /app/.venv

# Копируем requirements из папки backend
COPY backend/requirements.txt .

# Устанавливаем зависимости в venv
RUN /app/.venv/bin/pip install --no-cache-dir -r requirements.txt

# === STAGE 2: Runtime ===
FROM python:3.12-slim

WORKDIR /app

# Системные зависимости для runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    libmagic1 \
    libjpeg62-turbo \
    zlib1g \
    libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

# Создаём non-root пользователя
RUN useradd -m -u 1000 appuser

# Копируем venv из builder
COPY --from=builder /app/.venv /app/.venv

# Копируем код приложения
COPY backend /app/backend

# Создаём директории для данных
RUN mkdir -p /app/data/uploads /app/data/logs && \
    chown -R appuser:appuser /app

# Переключаемся на appuser
USER appuser

# Добавляем venv в PATH
ENV PATH="/app/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Команда запуска
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]