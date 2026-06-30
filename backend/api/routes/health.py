from fastapi import APIRouter

from backend.schemas.health import HealthResponse
from backend.services.health_service import get_health_status

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return get_health_status()
