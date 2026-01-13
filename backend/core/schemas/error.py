# backend/core/schemas/error.py
from typing import Optional, Any, Dict
from pydantic import BaseModel


class ErrorDetails(BaseModel):
    code: str
    message: str
    fields: Optional[list[str]] = None  # Для 422 ошибки (какие поля неверны)
    # Позволяем добавлять любые дополнительные поля (например, headers для 401)
    extra: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """
    Стандартизированный ответ с ошибкой.
    Используется для документации Swagger (400, 401, 404, 500).
    """

    error: ErrorDetails
