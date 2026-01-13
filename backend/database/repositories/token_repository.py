from typing import Optional
import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from backend.database.models.models import RefreshToken

class TokenRepository:
    """
    SQLAlchemy implementation of ITokenRepository.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: uuid.UUID, token: str, expires_at: datetime) -> RefreshToken:
        db_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        self.session.add(db_token)
        await self.session.commit()
        await self.session.refresh(db_token)
        return db_token

    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        stmt = select(RefreshToken).where(RefreshToken.token == token)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, token: str) -> None:
        stmt = delete(RefreshToken).where(RefreshToken.token == token)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_all_for_user(self, user_id: uuid.UUID) -> None:
        stmt = delete(RefreshToken).where(RefreshToken.user_id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
