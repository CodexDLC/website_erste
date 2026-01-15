from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from backend.apps.users.schemas.token import RefreshTokenRequest, Token
from backend.apps.users.schemas.user import UserCreate, UserResponse
from backend.apps.users.services.auth_service import AuthService
from backend.core.exceptions import AuthException
from backend.dependencies.auth import get_auth_service

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_new_user(user_in: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    """
    Register a new user.
    """
    logger.info(f"AuthRouter | action=register_request email={user_in.email}")
    return await auth_service.register_user(user_in)


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    OAuth2 compatible token login.
    """
    logger.info(f"AuthRouter | action=login_request email={form_data.username}")

    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise AuthException(detail="Incorrect email or password")

    tokens = await auth_service.create_tokens(user)

    return tokens


@router.post("/refresh", response_model=Token)
async def refresh_token(token_in: RefreshTokenRequest, auth_service: AuthService = Depends(get_auth_service)):
    """
    Get new access/refresh tokens.
    """
    logger.info("AuthRouter | action=refresh_request")
    return await auth_service.refresh_token(token_in.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(token_in: RefreshTokenRequest, auth_service: AuthService = Depends(get_auth_service)):
    """
    Logout user.
    """
    logger.info("AuthRouter | action=logout_request")
    await auth_service.logout(token_in.refresh_token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
