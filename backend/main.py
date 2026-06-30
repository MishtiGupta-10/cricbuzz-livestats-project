from fastapi import FastAPI

from backend.api.routes import health
from backend.core.config import settings
from backend.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for the CricInsight cricket analytics platform.",
)

app.include_router(health.router, prefix=settings.api_prefix, tags=["health"])


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "CricInsight API is running",
        "docs": "/docs",
        "health": f"{settings.api_prefix}/health",
    }
