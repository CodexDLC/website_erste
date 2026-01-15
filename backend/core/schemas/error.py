# backend/core/schemas/error.py
from typing import Any

from pydantic import BaseModel


class ErrorDetails(BaseModel):
    code: str
    message: str
    fields: list[str] | None = None  # Для 422 ошибки (какие поля неверны)
    # Позволяем добавлять любые дополнительные поля (например, headers для 401)
    extra: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    """
    Стандартизированный ответ с ошибкой.
    Используется для документации Swagger (400, 401, 404, 500).
    """

    error: ErrorDetails
