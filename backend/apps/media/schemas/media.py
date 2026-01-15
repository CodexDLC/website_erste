from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FileRead(BaseModel):
    """
    Schema for reading File metadata (CAS).
    """
    hash: str
    size_bytes: int
    mime_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ImageRead(BaseModel):
    """
    Schema for reading Image metadata (User Asset).
    """
    id: UUID
    filename: str
    created_at: datetime
    # We might want to include file details here
    file: FileRead

    model_config = ConfigDict(from_attributes=True)
