from fastapi import APIRouter

health_router = APIRouter(
    tags=["health"],
    prefix="/health",
)


@health_router.get("/check", status_code=200, summary="Health check")
async def health_check():
    """Health check endpoint to see if service is healthy and running"""
    return {
        "status": True,
        "message": "Service is healthy and running",
    }
