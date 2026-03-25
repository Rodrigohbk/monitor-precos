from fastapi import APIRouter
from app.api.v1.endpoints import auth, products , health


api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(products.router, prefix="/products", tags=["products"])