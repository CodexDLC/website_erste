from fastapi import APIRouter, Depends
from loguru import logger

from backend.apps.users.schemas.user import UserResponse
from backend.apps.users.dependencies import get_current_user
from backend.database.models.models import User

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user profile.
    """
    logger.info(f"UserRouter | action=get_me user_id={current_user.id}")
    return current_user
