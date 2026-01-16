from sqlalchemy.ext.asyncio import AsyncSession

from shop_app.repositories import CategoryRepository
from shop_app.schemas import CategoriesAll


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.cat_repo: CategoryRepository = CategoryRepository(session=session)

    async def get_all_categories(self) -> CategoriesAll:
        cats = await self.cat_repo.get_all_categories()
        if cats is None:
            return CategoriesAll(status=True, message="No categories found", categories=[], total_count=0)
        return CategoriesAll(
            status=True, message=f"Found {len(cats)} categories", categories=cats, total_count=len(cats)
        )
