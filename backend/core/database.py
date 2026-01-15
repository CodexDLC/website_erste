# backend/core/database.py
from collections.abc import AsyncGenerator
from typing import Any
from urllib.parse import urlparse, urlunparse

from loguru import logger as log
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..database.models.base import Base
from .config import settings

connect_args: dict[str, Any] = {
    "prepared_statement_cache_size": 0,
}

db_url = settings.DATABASE_URL

# Fix for asyncpg not supporting 'sslmode' and other params in URL
if "sslmode" in db_url:
    connect_args["ssl"] = "require"
    try:
        parsed = urlparse(db_url)
        db_url = urlunparse(parsed._replace(query=""))
    except Exception as e:
        log.warning(f"Failed to parse DB URL: {e}. Using original.")

pool_settings: dict[str, Any] = {
    "pool_size": 20,
    "max_overflow": 10,
    "pool_pre_ping": True,
}

# We disable echo because we handle logging via Loguru interceptor
async_engine = create_async_engine(
    db_url,
    echo=False,  # Changed from settings.DEBUG to False to avoid duplicate logs
    connect_args=connect_args,
    **pool_settings,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def create_db_tables() -> None:
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        log.info("Tables created successfully via SQLAlchemy")
    except SQLAlchemyError as e:
        log.error(f"Error creating tables: {e}")
