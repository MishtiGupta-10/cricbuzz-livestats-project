from backend.core.config import settings
from backend.schemas.health import HealthResponse


def get_health_status() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )
