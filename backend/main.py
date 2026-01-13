# backend/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .core.config import settings
from .core.exceptions import BaseAPIException, api_exception_handler
from .core.database import async_engine, create_db_tables
from .core.logger import setup_loguru
from .router import api_router, tags_metadata

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_loguru()
    logger.info("🚀 Server starting... Project: {name}", name=settings.PROJECT_NAME)
    
    if settings.DEBUG:
        logger.debug("🐛 Debug mode is ENABLED")
    
    logger.info("Connecting to Database and creating tables...")
    await create_db_tables()
    
    yield
    
    logger.info("🛑 Server shutting down... Closing DB connections...")
    await async_engine.dispose()
    logger.info("👋 Bye!")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=tags_metadata,  # Подключаем описания тегов
    lifespan=lifespan,
)

if settings.ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_exception_handler(BaseAPIException, api_exception_handler)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME}

@app.get("/", tags=["System"])
async def root():
    return {"message": "Welcome to PinLite API. Go to /docs for Swagger."}
