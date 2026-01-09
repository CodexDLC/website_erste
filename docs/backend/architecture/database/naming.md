[🏠 Home](../../../index.md) > [Backend](../../index.md) > [Architecture](../index.md) > [Database](./index.md)

# 🏷️ Naming Conventions

Правила именования в базе данных.

## Таблицы
*   **Snake Case**: `users`, `refresh_tokens`, `user_profiles`.
*   **Plural**: Названия во множественном числе (`users`, а не `user`).

## Поля
*   **PK**: `id` (обычно UUID или BigInt).
*   **FK**: `entity_id` (например, `user_id`, `image_id`).
*   **Boolean**: Префикс `is_` или `has_` (например, `is_active`, `has_access`).
*   **Date**: Суффикс `_at` для timestamp (`created_at`) или `_date` для date.

---
[🏠 Вернуться на главную](../../../index.md)
