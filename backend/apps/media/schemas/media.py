from datetime import datetime
from uuid import UUID

from pydantic import computed_field

from backend.core.schemas.base import BaseResponse


class FileRead(BaseResponse):
    """
    Schema for reading File metadata (CAS).
    """

    hash: str
    size_bytes: int
    mime_type: str
    created_at: datetime


class ImageRead(BaseResponse):
    """
    Schema for reading Image metadata (User Asset).
    """

    id: UUID
    filename: str
    created_at: datetime
    file: FileRead

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
