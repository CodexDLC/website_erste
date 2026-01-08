[🏠 Home](../index.md)

# 🐍 Backend Documentation

## 📂 Project Structure & Navigation

Ниже представлена структура проекта. Кликайте на папки для перехода к документации.

### Application Code
```text
backend/
 ┣ 📂 [core](./architecture/core/index.md)             # Инфраструктурный слой (Config, DB Connect, Logs)
 ┃ ┣ 📜 config.py
 ┃ ┣ 📜 database.py
 ┃ ┣ 📜 logger.py
 ┃ ┗ 📜 security.py
 ┃
 ┣ 📂 database                                         # Слой данных (Infrastructure)
 ┃ ┣ 📂 models                                         # SQLAlchemy Models (Таблицы БД)
 ┃ ┗ 📂 repositories                                   # Реализация репозиториев
 ┃
 ┣ 📂 [apps](./architecture/index.md)                  # Доменный слой (Бизнес-фичи)
 ┃ ┣ 📂 [users](./architecture/domains/users.md)       # Домен: Пользователи
 ┃ ┃ ┣ 📂 api                                          # Controllers (Routers)
 ┃ ┃ ┣ 📂 contracts                                    # Interfaces (Repository Protocols)
 ┃ ┃ ┣ 📂 services                                     # Business Logic
 ┃ ┃ ┗ 📂 schemas                                      # DTO (Pydantic)
 ┃ ┃
 ┃ ┗ 📂 [media](./architecture/domains/media/index.md) # Домен: Медиа
 ┃   ┣ 📂 api
 ┃   ┣ 📂 contracts
 ┃   ┣ 📂 services
 ┃   ┗ 📂 schemas
 ┃
 ┗ 📜 main.py
```

### Infrastructure & Storage
```text
root/
 ┣ 📂 [nginx](../nginx/README.md)             # Конфигурация прокси
 ┃ ┗ 📜 nginx.conf
 ┃
 ┗ 📂 data              # Persistent Storage (Volumes)
   ┣ 📂 uploads         # Здесь физически лежат картинки (cat.png, dog.png)
   ┗ 📂 logs            # Логи Nginx и Backend
```

## 📑 Management & Planning
*   **[📅 Management](./management/index.md)** (Roadmap, Tasks, Tech Debt)
*   **[🏗️ Architecture Details](./architecture/index.md)** (Deep dive into flows & domains)

---
[🏠 Вернуться на главную](../index.md)
