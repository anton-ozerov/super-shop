from sqlalchemy.ext.asyncio import AsyncSession

from shop_app.repositories import CategoryRepository
from shop_app.schemas import CategoriesAll


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.cat_repo: CategoryRepository = CategoryRepository(session=session)

    async def get_all_categories(self, page, per_page) -> CategoriesAll:
        cats, pagination = await self.cat_repo.get_all_categories(page, per_page)
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
