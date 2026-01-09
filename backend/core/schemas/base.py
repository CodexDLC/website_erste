# backend/core/schemas/base.py
from typing import Any
from pydantic import BaseModel, ConfigDict

class BaseRequest(BaseModel):
    """
    Контракт для ВХОДЯЩИХ данных (Request Body).
    Используется для валидации того, что присылает фронтенд (UserCreate, Login).
    """
    # Разрешаем передавать поля по alias (если вдруг на фронте camelCase)
    model_config = ConfigDict(populate_by_name=True)

class BaseResponse(BaseModel):
    """
    Контракт для ИСХОДЯЩИХ ответов (Response Body).
    Используется, чтобы превращать объекты БД (SQLAlchemy) в JSON.
    """
    # Самая важная настройка: разрешает читать данные из атрибутов класса (ORM)
    model_config = ConfigDict(from_attributes=True)
