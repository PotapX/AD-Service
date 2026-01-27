"""Роутер для проверки работоспособности сервиса."""
from datetime import datetime
from fastapi import APIRouter
from schemas.response import HealthResponse

router = APIRouter(tags=["health"])

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Проверка работоспособности",
    description=""
)
async def health_check() -> HealthResponse:
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )