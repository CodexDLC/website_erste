[🏠 Home](../../../index.md) > [Backend](../../index.md) > [Architecture](../index.md) > [Database](./index.md)

# 🔄 Database Migrations

Документация по работе с миграциями базы данных через Alembic.

## 📋 Содержание
- [Автоматические миграции](#автоматические-миграции)
- [Создание миграций](#создание-миграций)
- [Применение миграций](#применение-миграций)
- [Команды Alembic](#команды-alembic)
- [Конфигурация](#конфигурация)

---

## Автоматические миграции

Проект настроен на автоматический запуск миграций при старте приложения.

### AUTO_MIGRATE флаг

Контролируется через переменную окружения `AUTO_MIGRATE` в `backend/core/config.py`:

```python
AUTO_MIGRATE: bool = True  # По умолчанию включено
```

**Поведение:**
- `AUTO_MIGRATE=True` — миграции выполняются автоматически при старте приложения
- `AUTO_MIGRATE=False` — миграции нужно запускать вручную

### Когда использовать

**✅ Включено (True):**
- Локальная разработка
- Staging окружение
- Простые проекты

**❌ Выключено (False):**
- Production окружение с критичными данными
- Когда нужен контроль над миграциями
- CI/CD пайплайны с отдельным этапом миграций

---

## Создание миграций

### Автогенерация миграции

Alembic автоматически определяет изменения в моделях SQLAlchemy:

```bash
# Локально
docker-compose exec backend alembic revision --autogenerate -m "Описание изменений"

# Production
docker compose -f docker-compose.prod.yml exec -T backend alembic revision --autogenerate -m "Описание изменений"
```

### Пустая миграция (для ручных изменений)

```bash
docker-compose exec backend alembic revision -m "Описание изменений"
```

### Рекомендации по сообщениям

- Используйте глаголы в повелительном наклонении: `"Add user avatar field"`, `"Remove deprecated columns"`
- Будьте конкретны: `"Add indexes to user.email and user.username"`
- Группируйте связанные изменения в одну миграцию

---

## Применение миграций

### Автоматически (при AUTO_MIGRATE=True)

Миграции применяются автоматически при старте приложения в `backend/main.py`:

```python
async def lifespan(app: FastAPI):
    logger.info("🚀 Server starting... Project: PinLite")

    if settings.AUTO_MIGRATE:
        logger.info("Running database migrations (AUTO_MIGRATE=True)...")
        await run_alembic_migrations()
    else:
        logger.warning("⚠️ AUTO_MIGRATE=False: Skipping migrations.")
```

### Вручную

```bash
# Применить все миграции до последней
docker-compose exec backend alembic upgrade head

# Применить конкретную миграцию
docker-compose exec backend alembic upgrade <revision_id>

# Откатить на одну миграцию назад
docker-compose exec backend alembic downgrade -1

# Откатить до конкретной ревизии
docker-compose exec backend alembic downgrade <revision_id>
```

---

## Команды Alembic

### Просмотр истории

```bash
# Показать текущую ревизию
docker-compose exec backend alembic current

# Показать историю миграций
docker-compose exec backend alembic history

# Показать детали конкретной миграции
docker-compose exec backend alembic show <revision_id>
```

### Проверка состояния

```bash
# Показать список невыполненных миграций
docker-compose exec backend alembic heads

# Проверить что миграции синхронизированы
docker-compose exec backend alembic check
```

---

## Конфигурация

### Структура файлов

```
backend/
├── alembic/
│   ├── env.py              # Конфигурация окружения Alembic
│   ├── script.py.mako      # Шаблон для новых миграций
│   └── versions/           # Папка с миграциями
│       └── xxxx_initial_migration.py
├── alembic.ini             # Основной конфиг Alembic
└── core/
    ├── config.py           # Содержит AUTO_MIGRATE
    └── database.py         # run_alembic_migrations()
```

### alembic/env.py

Основные настройки:

```python
# Импорт настроек проекта
from backend.core.config import settings
from backend.core.database import Base

# Импорт всех моделей для автогенерации
import backend.database.models  # noqa: F401

# URL базы данных из настроек
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Метаданные SQLAlchemy
target_metadata = Base.metadata
```

### Асинхронное выполнение

Миграции запускаются асинхронно через `asyncio.to_thread()` в `backend/core/database.py`:

```python
async def run_alembic_migrations() -> None:
    import asyncio
    from alembic import command
    from alembic.config import Config
    from pathlib import Path

    def _run_sync_migrations():
        try:
            alembic_cfg_path = Path(__file__).parent.parent / "alembic.ini"
            if not alembic_cfg_path.exists():
                logger.warning("alembic.ini not found")
                return
            alembic_cfg = Config(str(alembic_cfg_path))
            command.upgrade(alembic_cfg, "head")
            logger.info("Database | action=run_migrations status=success")
        except Exception as exc:
            logger.error(f"Database | action=run_migrations status=failed error={exc}")
            raise

    await asyncio.to_thread(_run_sync_migrations)
```

---

## CI/CD интеграция

### GitHub Actions

В `.github/workflows/cd-release.yml` миграции запускаются после деплоя:

```yaml
- name: Deploy and Run Migrations
  run: |
    docker compose -f docker-compose.prod.yml up -d --wait
    docker compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
```

### Рекомендации для Production

1. **Отключите AUTO_MIGRATE** в production:
   ```bash
   AUTO_MIGRATE=False
   ```

2. **Запускайте миграции в CI/CD** после деплоя:
   ```bash
   docker compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
   ```

3. **Делайте бэкап** перед миграциями:
   ```bash
   pg_dump -U user -d database > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

4. **Тестируйте миграции** на staging окружении перед production

---

## Troubleshooting

### Миграции не применяются автоматически

1. Проверьте `AUTO_MIGRATE`:
   ```bash
   docker-compose exec backend python -c "from backend.core.config import settings; print(settings.AUTO_MIGRATE)"
   ```

2. Проверьте логи:
   ```bash
   docker-compose logs backend | grep migration
   ```

### Конфликты миграций

При работе в команде могут возникнуть конфликты веток миграций:

```bash
# Объединить две ветки миграций
docker-compose exec backend alembic merge -m "Merge migrations" <revision1> <revision2>
```

### Миграция не накатывается

1. Проверьте текущую ревизию:
   ```bash
   docker-compose exec backend alembic current
   ```

2. Проверьте список доступных миграций:
   ```bash
   docker-compose exec backend alembic heads
   ```

3. Попробуйте применить конкретную ревизию:
   ```bash
   docker-compose exec backend alembic upgrade <revision_id>
   ```

---

[🏠 Вернуться на главную](../../../index.md) | [⬆️ Database](./index.md)
