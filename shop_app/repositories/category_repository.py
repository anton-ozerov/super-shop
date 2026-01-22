import logging
from math import ceil

from sqlalchemy import asc, func, nulls_last, select
from sqlalchemy.ext.asyncio import AsyncSession

from shop_app.database import Category
from shop_app.schemas import CategoryOut, PaginationSchema

logger = logging.getLogger(__name__)


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_categories(self, page, per_page) -> tuple[list[CategoryOut] | None, PaginationSchema]:
        logs_extra = {
            "method": "get_all_categories",
            "service": "category_repository",
            "page": page,
            "per_page": per_page,
        }

        page = max(1, page)
        per_page = max(1, per_page)

        offset = (page - 1) * per_page

        pagination = await self._get_pagination(page, per_page)

        if page > pagination.total_pages > 0:
            logger.warning(
                "Requested page exceeds total pages", extra={**logs_extra, "total_pages": pagination.total_pages}
            )
            return None, pagination

        query = (
            select(Category)
            .order_by(nulls_last(asc(Category.sort_order)), asc(Category.name))
            .limit(per_page)
            .offset(offset)  # starting with offset number based on pagination given by user
        )

        logger.info("Fetching categories from the database", extra=logs_extra)

        result = await self.session.execute(query)
        categories = result.scalars().all()

        pagination.current_items = len(categories)

        if categories:
            logs_extra["count"] = str(len(categories))
            logger.info("Categories found in the database", extra=logs_extra)
            return [CategoryOut.model_validate(cat) for cat in categories], pagination

        logger.warning("No categories found in the database", extra=logs_extra)
        return None, pagination

    async def _get_pagination(self, page, per_page) -> PaginationSchema:
        result = await self.session.execute(select(func.count(Category.id)))
        total_items = result.scalar() or 0

        total_pages = ceil(total_items / per_page)

        has_next = page < total_pages
        has_previous = page > 1

        return PaginationSchema(
            page=page,
            total_pages=total_pages,
            per_page=per_page,
            total_items=total_items,
            current_items=0,  # will be updated later
            has_next=has_next,
            has_previous=has_previous,
        )
