import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from backend.core.database import get_db
from backend.database.models.base import Base
from backend.main import app
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

# --- TEST DATABASE CONFIG ---
# Read from ENV (for CI), otherwise use default (for local run)
# In CI we pass DATABASE_URL=postgresql+asyncpg://postgres:test_password@localhost:5432/test_db
DEFAULT_TEST_DB_URL = "postgresql+asyncpg://postgres:postgres@localhost:5433/test_db"
TEST_DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_TEST_DB_URL)

# Create separate engine for tests
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,  # Important for tests to close connections immediately
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Database fixture.
    Creates tables before test and drops them after.
    """
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session
        # Rollback transaction after test (optional, since we drop tables)
        await session.rollback()

    # Drop tables (cleanup)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    HTTP Client fixture for integration tests.
    Overrides get_db dependency with test session.
    """
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # Use ASGITransport for direct app calls without network requests
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
