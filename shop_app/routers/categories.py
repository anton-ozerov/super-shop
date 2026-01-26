import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from shop_app.database import get_async_session
from shop_app.schemas import CategoriesAll
from shop_app.services import CategoryService

logger = logging.getLogger(__name__)

categories_router = APIRouter(
    tags=["categories"],
    prefix="/categories",
)


@categories_router.get("/", response_model=CategoriesAll)
async def categories(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    per_page: Annotated[int, Query(ge=1, le=100, description="Count items per page")] = 10,
):
    """All categories endpoint with pagination"""
    logger.debug("Receiving all categories")
    try:
        cat_service = CategoryService(session=session)
        cats = await cat_service.get_all_categories(page, per_page)
        return cats
    except Exception as e:
        logger.error(
            "Failed to receive categories",
            exc_info=True,
            extra={
                "error_message": str(e),
            },
        )
        raise HTTPException(status_code=500, detail="Internal server error") from e
