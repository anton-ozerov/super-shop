import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

health_router = APIRouter(
    tags=["health"],
    prefix="/health",
)


@health_router.get("/check", status_code=200, summary="Health check")
async def health_check():
    """Health check endpoint to see if service is healthy and running"""
    logger.info("Health check endpoint called and it is healthy", extra={"service": "health"})
    return {
        "status": True,
        "message": "Service is healthy and running",
    }
