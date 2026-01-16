# backend/core/schemas/error.py
from typing import Any

from pydantic import BaseModel, Field


class ErrorDetails(BaseModel):
    code: str = Field(..., description="Internal error code (e.g. 'user_not_found')")
    message: str = Field(..., description="Human-readable error message")
    fields: list[Any] | None = Field(None, description="List of validation errors (for 422)")
    
    # Allow extra fields
    model_config = {"extra": "allow"}


class ErrorResponse(BaseModel):
    """
    Standardized error response structure.
    Used for Swagger documentation (400, 401, 403, 404, 500).
    """
    error: ErrorDetails
