from fastapi import FastAPI

import contextlib

from backend.api.routes import health, matches, sync, analytics
from backend.core.config import settings
from backend.core.logging import configure_logging
from backend.core.exceptions import CricInsightError
from backend.core.errors import cricinsight_exception_handler, generic_exception_handler
from backend.sync.scheduler import scheduler

configure_logging()

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the sync scheduler on app startup
    await scheduler.start()
    yield
    # Stop it on shutdown
    await scheduler.stop()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for the CricInsight cricket analytics platform.",
    lifespan=lifespan
)

# Exception handlers
app.add_exception_handler(CricInsightError, cricinsight_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Routers
app.include_router(health.router, prefix=settings.api_prefix, tags=["health"])
app.include_router(matches.router, prefix=f"{settings.api_prefix}/matches", tags=["matches"])
app.include_router(sync.router, prefix=f"{settings.api_prefix}/sync", tags=["sync"])
app.include_router(analytics.router, prefix=f"{settings.api_prefix}")


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "CricInsight API is running",
        "docs": "/docs",
        "health": f"{settings.api_prefix}/health",
        "matches": f"{settings.api_prefix}/matches/live",
    }
