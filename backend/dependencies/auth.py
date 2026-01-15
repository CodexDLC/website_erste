import uuid
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apps.users.contracts.token_repository import ITokenRepository
from backend.apps.users.contracts.user_repository import IUserRepository
from backend.apps.users.services.auth_service import AuthService
from backend.core.config import settings
from backend.core.database import get_db
from backend.core.exceptions import AuthException
from backend.core.security import ALGORITHM
from backend.database.models import User
from backend.database.repositories.token_repository import TokenRepository
from backend.database.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> IUserRepository:
    """
    Dependency provider for User Repository.
    """
    return UserRepository(session=db)


def get_token_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ITokenRepository:
    """
    Dependency provider for Token Repository.
    """
    return TokenRepository(session=db)


def get_auth_service(
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
    token_repository: Annotated[ITokenRepository, Depends(get_token_repository)],
) -> AuthService:
    """
    Dependency provider for Auth Service.
    """
    return AuthService(user_repository=user_repository, token_repository=token_repository)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    """
    Dependency to get the current authenticated user from the JWT token.
    Returns the SQLAlchemy User model instance.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise AuthException(detail="Could not validate credentials")

        # Validate that sub is a valid UUID
        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError as e:
            raise AuthException(detail="Invalid token subject") from e

    except JWTError as e:
        raise AuthException(detail="Could not validate credentials") from e

    # Fix: Use get_by_id instead of get_by_email
    user = await auth_service.user_repository.get_by_id(user_id=user_id)
    if user is None:
        raise AuthException(detail="User not found")

    return user
