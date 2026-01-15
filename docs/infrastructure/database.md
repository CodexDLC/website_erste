[🏠 Home](../index.md) > [Infrastructure](./index.md)

# 🗄️ Database Configuration

В качестве основной базы данных используется **PostgreSQL**.

## ☁️ Neon (Serverless Postgres)
На текущем этапе (MVP) мы используем облачную базу данных [Neon.tech](https://neon.tech).

### Подключение
Строка подключения задается в переменной окружения `DATABASE_URL` в файле `.env`.

```ini
DATABASE_URL=postgresql+asyncpg://user:password@ep-host-123.aws.neon.tech/dbname?ssl=require
```

*   **Driver:** `asyncpg` (для асинхронной работы с SQLAlchemy).
*   **SSL:** Обязателен (`ssl=require`).

## 🛠️ Migrations (Alembic)
Управление схемой БД осуществляется через Alembic.

### Основные команды
*   **Создать миграцию:**
    ```bash
    docker-compose exec backend alembic revision --autogenerate -m "description"
    ```
*   **Применить миграции:**
    ```bash
    docker-compose exec backend alembic upgrade head
    ```

---
[⬅️ Назад к Infrastructure](./index.md)
