# backend/core/database.py
from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger as log

from .config import settings

connect_args: dict[str, Any] = {
    "prepared_statement_cache_size": 0,
}

if "ssl" in settings.DATABASE_URL: 
    connect_args["ssl"] = "require"

pool_settings: dict[str, Any] = {
    "pool_size": 20,
    "max_overflow": 10,
    "pool_pre_ping": True,
}

async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=connect_args,
    **pool_settings,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

class Base(DeclarativeBase):
    pass

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
