from uuid import UUID

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from fastapi import Path as PathParam
from fastapi.responses import FileResponse

from backend.apps.media.schemas.media import ImageRead
from backend.apps.media.services.media_service import MediaService
from backend.core.exceptions import NotFoundException
from backend.database.models import User
from backend.dependencies.auth import get_current_user
from backend.dependencies.media import get_media_service

router = APIRouter()


@router.post("/upload", response_model=ImageRead, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: MediaService = Depends(get_media_service),
) -> ImageRead:
    """
    Upload a new image.
    """
    return await service.upload_image(user_id=current_user.id, file=file)


@router.get("/feed", response_model=list[ImageRead])
async def get_feed(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: MediaService = Depends(get_media_service),
) -> list[ImageRead]:
    """
    Get public feed of images.
    """
    return await service.get_feed(limit=limit, offset=offset)


@router.get("/my", response_model=list[ImageRead])
async def get_my_gallery(
    current_user: User = Depends(get_current_user),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: MediaService = Depends(get_media_service),
) -> list[ImageRead]:
    """
    Get current user's gallery.
    """
    return await service.get_user_gallery(user_id=current_user.id, limit=limit, offset=offset)


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_id: UUID = PathParam(...),
    current_user: User = Depends(get_current_user),
    service: MediaService = Depends(get_media_service),
) -> None:
    """
    Delete an image.
    """
    await service.delete_image(user_id=current_user.id, image_id=image_id)


# --- Serving Files (Dev Mode / Fallback) ---


@router.get("/{file_hash}", response_class=FileResponse)
async def get_file(
    file_hash: str = PathParam(..., min_length=64, max_length=64),
    service: MediaService = Depends(get_media_service),
) -> FileResponse:
    """
    Serve original file by hash.
    """
    # Access private method to resolve path (pragmatic choice for serving)
    # In production, Nginx should handle this mapping.
    path = service._get_storage_path(file_hash)
    if not path.exists():
        raise NotFoundException(detail="File not found")

    return FileResponse(path)


@router.get("/{file_hash}/thumb", response_class=FileResponse)
async def get_thumbnail(
    file_hash: str = PathParam(..., min_length=64, max_length=64),
    service: MediaService = Depends(get_media_service),
) -> FileResponse:
    """
    Serve thumbnail by hash.
    """
    path = service._get_thumbnail_path(file_hash)
    if not path.exists():
        # Fallback to original if thumb missing (or 404)
        # Let's return 404 to be strict
        raise NotFoundException(detail="Thumbnail not found")

    return FileResponse(path)
