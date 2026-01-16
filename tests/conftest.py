import asyncio
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
# Используем локальный Docker контейнер на порту 5433
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5433/test_db"

# Создаем отдельный engine для тестов
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,  # Важно для тестов, чтобы закрывать соединения сразу
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
    Фикстура базы данных.
    Создает таблицы перед тестом и удаляет после.
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
    Фикстура HTTP клиента для интеграционных тестов.
    Переопределяет зависимость get_db на тестовую сессию.
    """
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    # Используем ASGITransport для прямого вызова приложения без сетевых запросов
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()
