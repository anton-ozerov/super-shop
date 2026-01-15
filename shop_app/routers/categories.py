import logging

from fastapi import APIRouter, Depends, HTTPException

from shop_app.repositories import CategoryRepository
from shop_app.schemas import CategoriesAll
from shop_app.services import CategoryService

logger = logging.getLogger()

categories_router = APIRouter(
    tags=["categories"],
    prefix="/categories",
)


@categories_router.get("/", response_model=CategoriesAll)
async def categories(cat_repo: CategoryRepository = Depends(CategoryRepository)):  # noqa
    """All categories endpoint"""
    logger.info("Receiving all categories")
    try:
        cats = await CategoryService.get_all_categories(cat_repo=cat_repo)
        if cats is None:
            return CategoriesAll(status=True, message="No categories found", categories=[], total_count=0)
        return cats
    except Exception as e:
        logger.error(
            "Failed to receive all categories",
            exc_info=True,
            extra={
                "error_message": str(e),
            },
        )
        raise HTTPException(status_code=500, detail="Internal server error") from e
