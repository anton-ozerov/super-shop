import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from shop_app.database import get_async_session
from shop_app.schemas import GetProductsResponseSchema
from shop_app.services import ProductService

logger = logging.getLogger(__name__)


router = APIRouter(
    tags=["products"],
    prefix="/products",
)


@router.get("/", response_model=GetProductsResponseSchema)
async def get_all_not_deleted_products(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    per_page: Annotated[int, Query(ge=1, le=100, description="Number of items per page")] = 10,
):
    """Endpoint to get not deleted products"""
    logger.debug(
        "Get all products endpoint called",
        extra={"service": "product_router", "method": "get_all_products", "page": page, "per_page": per_page},
    )
    product_service = ProductService(session=session)
    products = await product_service.get_all_categories(page=page, per_page=per_page)
    logger.info(
        "Get all products endpoint completed",
        extra={
            "service": "product_router",
            "method": "get_all_products",
            "page": page,
            "per_page": per_page,
            "total_count": products.pagination.total_items,
            "current_count": products.pagination.current_items,
        },
    )
    return products
