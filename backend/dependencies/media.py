from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apps.media.contracts.media_repository import IMediaRepository
from backend.apps.media.services.media_service import MediaService
from backend.core.database import get_db
from backend.database.repositories.media_repository import MediaRepository


def get_media_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> IMediaRepository:
    """
    Dependency provider for Media Repository.
    """
    return MediaRepository(session=db)


def get_media_service(
    repository: Annotated[IMediaRepository, Depends(get_media_repository)],
) -> MediaService:
    """
    Dependency provider for Media Service.
    """
    return MediaService(repository=repository)
