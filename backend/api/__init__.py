from fastapi import APIRouter
from backend.api import health, evalapi, ui
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(evalapi.router, prefix="/api", tags=["evalapi"])
api_router.include_router(ui.router, tags=["ui"])
