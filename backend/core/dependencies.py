# backend/core/dependencies.py
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from .config import settings, Settings


@dataclass
class APIContext:
    db: AsyncSession
    settings: Settings


async def get_context(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> APIContext:
    return APIContext(
        db=db,
        settings=settings,
    )


Ctx = Annotated[APIContext, Depends(get_context)]
