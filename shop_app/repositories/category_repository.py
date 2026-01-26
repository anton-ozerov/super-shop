import logging

from sqlalchemy import asc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from shop_app.database import Category
from shop_app.schemas import CategoryOut

logger = logging.getLogger(__name__)


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_categories(self, page, per_page) -> tuple[list[CategoryOut] | None, int | None]:
        logs_extra = {
            "method": "get_all_categories",
            "service": "category_repository",
            "page": page,
            "per_page": per_page,
        }

        offset = (page - 1) * per_page

        cats_on_pages = (
            select(Category)
            .order_by(asc(Category.sort_order), asc(Category.name))
            .limit(per_page)
            .offset(offset)  # starting with offset number based on pagination given by user
        )

        logger.info("Fetching categories from the database", extra=logs_extra)

        result = await self.session.execute(cats_on_pages)
        categories = result.scalars().all()

        result_total_cats = await self.session.execute(select(func.count(Category.id)))
        total_items = result_total_cats.scalar() or 0

        if categories and total_items:
            logs_extra["count"] = str(len(categories))
            logger.info("Categories found in the database", extra=logs_extra)
            return [CategoryOut.model_validate(cat) for cat in categories], total_items

        elif total_items:
            logger.info("There are not categories on this page", extra=logs_extra)
            return None, total_items

        logger.warning("No categories found in the database", extra=logs_extra)
        return None, 0
