from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, status, Query, Path

from backend.dependencies.auth import get_current_user
from backend.database.models import User
from backend.apps.media.schemas.media import ImageRead
from backend.dependencies.media import get_media_service
from backend.apps.media.services.media_service import MediaService

router = APIRouter()


@router.post("/upload", response_model=ImageRead, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: MediaService = Depends(get_media_service),
):
    """
    Upload a new image.
    """
    return await service.upload_image(user_id=current_user.id, file=file)


@router.get("/feed", response_model=List[ImageRead])
async def get_feed(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: MediaService = Depends(get_media_service),
):
    """
    Get public feed of images.
    """
    return await service.get_feed(limit=limit, offset=offset)


@router.get("/my", response_model=List[ImageRead])
async def get_my_gallery(
    current_user: User = Depends(get_current_user),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: MediaService = Depends(get_media_service),
):
    """
    Get current user's gallery.
    """
    return await service.get_user_gallery(
        user_id=current_user.id, limit=limit, offset=offset
    )


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_id: UUID = Path(...),
    current_user: User = Depends(get_current_user),
    service: MediaService = Depends(get_media_service),
):
    """
    Delete an image.
    """
    await service.delete_image(user_id=current_user.id, image_id=image_id)
