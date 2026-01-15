import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Base schema for User data.
    Shared properties.
    """

    email: EmailStr


class UserCreate(UserBase):
    """
    Schema for User registration.
    """

    password: str = Field(..., min_length=8, description="User password")


class UserUpdate(BaseModel):
    """
    Schema for User update.
    """

    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """
    Schema for User response (public data).
    """

    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True
