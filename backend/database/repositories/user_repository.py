from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from backend.apps.users.contracts.user_repository import IUserRepository
from backend.database.models.models import User
from backend.apps.users.schemas.user import UserCreate

class UserRepository:
    """
    SQLAlchemy implementation of IUserRepository.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """
        Retrieve a user by their unique ID.
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        """
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user_in: UserCreate) -> User:
        """
        Create a new user in the database.
        WARNING: Assumes user_in.password holds the HASHED password.
        The Service layer is responsible for hashing before calling this.
        """
        db_user = User(
            email=user_in.email,
            hashed_password=user_in.password,
            is_active=True,
            is_superuser=False,
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user
