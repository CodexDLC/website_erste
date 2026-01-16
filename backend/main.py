# backend/main.py
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .core.config import settings
from .core.database import async_engine, create_db_tables
from .core.exceptions import BaseAPIException, api_exception_handler
from .core.logger import setup_loguru
from .core.schemas.error import ErrorResponse
from .router import api_router, tags_metadata


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    setup_loguru()
    logger.info("🚀 Server starting... Project: {name}", name=settings.PROJECT_NAME)

    if settings.DEBUG:
        logger.debug("🐛 Debug mode is ENABLED")
    else:
        logger.info("🔒 Production mode: Swagger UI is DISABLED")

    logger.info("Connecting to Database and creating tables...")
    await create_db_tables()

    yield

    logger.info("🛑 Server shutting down... Closing DB connections...")
    await async_engine.dispose()
    logger.info("👋 Bye!")


# --- DOCS CONFIGURATION ---
# Если DEBUG=False, отключаем документацию (None)
docs_url = "/docs" if settings.DEBUG else None
redoc_url = "/redoc" if settings.DEBUG else None
openapi_url = f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None

# --- GLOBAL ERROR RESPONSES ---
# Описываем, как выглядят ошибки в Swagger
responses: dict[int | str, dict[str, Any]] = {
    400: {"model": ErrorResponse, "description": "Bad Request"},
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    403: {"model": ErrorResponse, "description": "Forbidden"},
    404: {"model": ErrorResponse, "description": "Not Found"},
    409: {"model": ErrorResponse, "description": "Conflict"},
    422: {"model": ErrorResponse, "description": "Validation Error"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
}

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    responses=responses, # Подключаем глобальные схемы ошибок
)

# --- CORS SETUP ---
# Если DEBUG=True, разрешаем вообще всё (для локальной разработки)
if settings.DEBUG:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",  # Разрешает любой Origin
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
# Иначе используем список из конфига
elif settings.ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Mypy complains about incompatible type for exception handler, but it works at runtime
app.add_exception_handler(BaseAPIException, api_exception_handler) # type: ignore

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "app": settings.PROJECT_NAME}


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    if settings.DEBUG:
        return {"message": "Welcome to PinLite API. Go to /docs for Swagger."}
    return {"message": "Welcome to PinLite API."}
