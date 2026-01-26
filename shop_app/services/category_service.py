from sqlalchemy.ext.asyncio import AsyncSession

from shop_app.repositories import CategoryRepository
from shop_app.schemas import CategoriesAll
from shop_app.services.pagination_service import get_pagination


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.cat_repo: CategoryRepository = CategoryRepository(session=session)

    async def get_all_categories(self, page, per_page) -> CategoriesAll:
        cats, total_cats = await self.cat_repo.get_all_categories(page=page, per_page=per_page)
        if cats:
            current_items = len(cats)
        else:
            current_items = 0
        pagination = get_pagination(
            total_items=total_cats,
            page=page,
            per_page=per_page,
            current_items=current_items,
        )
        if cats is None:
            return CategoriesAll(
                status=True,
                pagination=pagination,
                message="No categories found",
                categories=[],
            )
        return CategoriesAll(
            status=True,
            pagination=pagination,
            message=f"Found {len(cats)} categories",
            categories=cats,
        )
