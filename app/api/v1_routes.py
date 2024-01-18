from fastapi import APIRouter

from app.api.endpoints import bills

api_router = APIRouter(prefix="/v1")

api_router.include_router(bills.router, tags=["bills"])
