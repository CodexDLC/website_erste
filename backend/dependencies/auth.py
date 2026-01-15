from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from backend.core.database import get_db
from backend.core.config import settings
from backend.core.security import ALGORITHM
from backend.core.exceptions import AuthException
from backend.apps.users.contracts.user_repository import IUserRepository
from backend.apps.users.contracts.token_repository import ITokenRepository
from backend.database.models import User
from backend.database.repositories.user_repository import UserRepository
from backend.database.repositories.token_repository import TokenRepository
from backend.apps.users.services.auth_service import AuthService
from backend.apps.users.schemas.token import TokenPayload


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
    return AuthService(
        user_repository=user_repository, token_repository=token_repository
    )


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
        email: str = payload.get("sub")
        if email is None:
            raise AuthException(detail="Could not validate credentials")
        token_data = TokenPayload(sub=email)
    except JWTError:
        raise AuthException(detail="Could not validate credentials")

    user = await auth_service.user_repository.get_by_email(email=token_data.sub)
    if user is None:
        raise AuthException(detail="User not found")

    return user
