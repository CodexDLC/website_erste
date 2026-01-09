# backend/router.py
from fastapi import APIRouter

# from backend.apps.users.routers import user_router
# from backend.apps.media.routers import media_router

api_router = APIRouter()

# Описание тегов для Swagger
tags_metadata = [
    {
        "name": "System",
        "description": "Health check and system info.",
    },
    {
        "name": "Users",
        "description": "Operations with users: **registration**, **login**, **profile**.",
    },
    {
        "name": "Media",
        "description": "Media management: **upload**, **gallery**, **processing**.",
    },
]

# api_router.include_router(user_router, prefix="/users", tags=["Users"])
# api_router.include_router(media_router, prefix="/media", tags=["Media"])

@api_router.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}
