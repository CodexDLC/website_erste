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
        Full URL to the original image.
        Assumes the API is mounted at /api/v1/media or similar,
        but here we return relative path from the router root.
        Frontend should prepend API base URL if needed, or we return absolute path if we knew the host.
        For now, we return relative path to the media router.
        """
        # Assuming the router is mounted at /media
        # We return the relative path that the frontend can use.
        # Since we don't know the full domain here easily without request context,
        # we'll return a path relative to the API root or absolute path if we assume a prefix.

        # Let's assume standard API structure: /api/v1/media/{hash}
        # But to be safe and relative-friendly:
        return f"/api/v1/media/{self.file.hash}"

    @computed_field
    def src(self) -> str:
        """
        URL to the thumbnail (for frontend gallery).
        """
        return f"/api/v1/media/{self.file.hash}/thumb"
