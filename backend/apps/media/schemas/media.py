from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, computed_field


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

    @computed_field
    def url(self) -> str:
        """
        Direct URL to the original image served by Nginx.
        Path: /media/storage/ab/cd/hash
        """
        h = self.file.hash
        # Sharding logic: first 2 chars, next 2 chars
        return f"/media/storage/{h[:2]}/{h[2:4]}/{h}"

    @computed_field
    def src(self) -> str:
        """
        Direct URL to the thumbnail served by Nginx.
        Path: /media/storage/ab/cd/hash_thumb.jpg
        """
        h = self.file.hash
        return f"/media/storage/{h[:2]}/{h[2:4]}/{h}_thumb.jpg"