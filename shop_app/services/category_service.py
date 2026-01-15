from shop_app.repositories import CategoryRepository
from shop_app.schemas import CategoriesAll


class CategoryService:
    @classmethod
    async def get_all_categories(cls, cat_repo: CategoryRepository) -> CategoriesAll:
        cats = await cat_repo.get_all_categories()
        if cats is None:
            return CategoriesAll(status=True, message="No categories found", categories=[], total_count=0)
        return CategoriesAll(
            status=True, message=f"Found {len(cats)} categories", categories=cats, total_count=len(cats)
        )
