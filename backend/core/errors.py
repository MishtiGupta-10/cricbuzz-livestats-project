from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

from backend.core.exceptions import (
    CricInsightError,
    CricbuzzClientError,
    CricbuzzAPIError,
    CricbuzzParseError
)

logger = logging.getLogger(__name__)

async def cricinsight_exception_handler(request: Request, exc: CricInsightError):
    """Base handler for all custom CricInsight errors."""
    logger.error(f"CricInsightError at {request.url.path}: {str(exc)}")
    
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if isinstance(exc, CricbuzzClientError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    elif isinstance(exc, CricbuzzAPIError):
        status_code = status.HTTP_502_BAD_GATEWAY
    elif isinstance(exc, CricbuzzParseError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """Fallback handler for unhandled exceptions."""
    logger.error(f"Unhandled exception at {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )
