import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shop_app.database import Category
from shop_app.schemas import CategoryOut

logger = logging.getLogger(__name__)


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_categories(self) -> list[CategoryOut] | None:
        logs_extra = {"method": "get_all_categories", "service": "category_repository"}
        logger.info("Fetching all categories from the database", extra=logs_extra)
        result = await self.session.execute(select(Category))
        categories = result.scalars().all()
        if categories:
            logs_extra["count"] = str(len(categories))
            logger.info("Categories found in the database", extra=logs_extra)
            return [CategoryOut.model_validate(cat) for cat in categories]
        logger.warning("No categories found in the database", extra=logs_extra)
        return None
