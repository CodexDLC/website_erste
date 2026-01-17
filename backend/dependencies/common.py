from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import Settings, settings
from backend.core.database import get_db


@dataclass
class APIContext:
    """
    Common API Context containing DB session and Settings.
    Useful for passing shared dependencies to services.
    """

    db: AsyncSession
    settings: Settings


async def get_context(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> APIContext:
    """
    Dependency provider for APIContext.
    """
    return APIContext(
        db=db,
        settings=settings,
    )


Ctx = Annotated[APIContext, Depends(get_context)]
