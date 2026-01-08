# backend/router.py
from fastapi import APIRouter

# from backend.apps.users.routers import user_router
# from backend.apps.media.routers import media_router

api_router = APIRouter()

# api_router.include_router(user_router, prefix="/users", tags=["Users"])
# api_router.include_router(media_router, prefix="/media", tags=["Media"])

@api_router.get("/health")
async def health_check():
    return {"status": "ok"}
