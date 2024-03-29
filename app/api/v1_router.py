from fastapi import APIRouter

from app.api.endpoints import bills, category, payment

api_router = APIRouter(prefix="/v1")

api_router.include_router(bills.router, tags=["bills"])
api_router.include_router(category.router, tags=["category"])
api_router.include_router(payment.router, tags=["payment"])
