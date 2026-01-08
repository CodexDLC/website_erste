[🏠 Home](../../../../index.md) > [Backend](../../../index.md) > [Architecture](../../index.md) > [Core](./index.md)

# ⚠️ Exceptions Module

**File:** `backend/core/exceptions.py`

Модуль определяет базовые классы исключений и глобальный обработчик ошибок.

## Концепция
Все ошибки API возвращаются в едином JSON-формате, удобном для фронтенда.

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid email format",
    "fields": ["email"]
  }
}
```

## Классы ошибок

*   **`BaseAPIException`**: Родительский класс.
*   **`NotFoundException` (404)**: Ресурс не найден.
*   **`ValidationException` (422)**: Ошибка бизнес-валидации.
*   **`BusinessLogicException` (409)**: Конфликт (например, дубликат).
*   **`PermissionDeniedException` (403)**: Нет прав.
*   **`AuthException` (401)**: Ошибка аутентификации.

## Использование

```python
from app.core.exceptions import NotFoundException

if not user:
    raise NotFoundException(detail="User not found")
```

---
[🏠 Вернуться на главную](../../../../index.md)
