[🏠 Home](../../index.md) > [Management](../index.md) > [Tasks](./index.md)

# 🛠️ Task: Swagger Error Schemas

**Status:** 📋 Backlog
**Priority:** Medium
**Related Tech Debt:** Missing Error Responses

## 📝 Описание проблемы
В текущей реализации Swagger (`/docs`) не отображает корректную структуру ответов с ошибками.
FastAPI по умолчанию показывает стандартную схему `{"detail": "string"}`, но наш проект использует кастомный обработчик исключений (`backend/core/exceptions.py`), который возвращает JSON вида:

```json
{
  "error": {
    "code": "auth_error",
    "message": "Authentication failed",
    "headers": { ... }
  }
}
```

Фронтенд-разработчики не видят эту структуру в документации и вынуждены смотреть исходный код бэкенда.

## 🎯 Цель
Обеспечить отображение реальной структуры ошибок (Error Response) в Swagger UI для всех эндпоинтов.

## 📋 План реализации

### 1. Создать схему ошибки
Создать файл `backend/core/schemas/error.py` (или использовать существующий `schemas` пакет).
Описать Pydantic-модели, соответствующие структуре ответа из `api_exception_handler`:

```python
from pydantic import BaseModel
from typing import Optional, Dict, Any

class ErrorDetail(BaseModel):
    code: str
    message: str
    # extra поля, если нужны (можно использовать model_extra)

class ErrorResponse(BaseModel):
    error: ErrorDetail
```

### 2. Обновить роутеры
В файлах API (например, `backend/apps/users/api/auth.py`) добавить параметр `responses` в декораторы роутов.

**Было:**
```python
@router.post("/login", response_model=Token)
```

**Станет:**
```python
from backend.core.schemas.error import ErrorResponse

@router.post(
    "/login",
    response_model=Token,
    responses={
        401: {"model": ErrorResponse, "description": "Incorrect email or password"},
        400: {"model": ErrorResponse, "description": "Validation Error"}
    }
)
```

### 3. Проверить результат
Запустить сервер, открыть `/docs` и убедиться, что при клике на коды ошибок (400, 401, 409) отображается наша кастомная JSON-схема, а не дефолтная.

---
[⬅️ Вернуться к списку задач](./index.md)
