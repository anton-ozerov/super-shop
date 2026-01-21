import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shop_app.database import Product
from shop_app.schemas import ProductOut, RepositoryGetNotDeletedProducts

logger = logging.getLogger(__name__)


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logs_extra: dict[str, str | int] = {"service": "product_repository"}

    async def get_not_deleted_products(self, page: int, per_page: int) -> RepositoryGetNotDeletedProducts:
        logs_extra = {**self.logs_extra, "page": page, "per_page": per_page, "method": "get_not_deleted_products"}

        try:
            logger.info("Fetching not deleted products from the database", extra=logs_extra)
            main_query = (
                select(Product)
                .options(selectinload(Product.marks))
                .where(Product.is_deleted.is_(False))
                .offset((page - 1) * per_page)
                .limit(per_page)
            )
            count_query = select(func.count()).select_from(Product).where(Product.is_deleted.is_(False))

            count_result = await self.session.execute(count_query)
            pagination_result = await self.session.execute(main_query)

            total_count = count_result.scalar_one()
            logs_extra["total_count"] = total_count

            products = pagination_result.scalars().all()
            if products:
                logs_extra["current_count"] = len(products)
                logger.info("Not deleted products found in the database", extra=logs_extra)
                return RepositoryGetNotDeletedProducts(
                    products=[ProductOut.model_validate(product) for product in products],
                    total_count=total_count,
                    current_count=len(products),
                )
            logger.warning("No products found in the database", extra=logs_extra)
        except Exception as e:
            logger.error(f"Error fetching not deleted products: {e}", extra=logs_extra, exc_info=True)

        return RepositoryGetNotDeletedProducts(
            products=[],
            total_count=0,
            current_count=0,
        )
