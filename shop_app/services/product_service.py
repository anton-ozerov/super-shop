from sqlalchemy.ext.asyncio import AsyncSession

from shop_app.repositories import ProductRepository
from shop_app.schemas import GetProductsResponseSchema
from shop_app.services import get_pagination


class ProductService:
    def __init__(self, session: AsyncSession):
        self.product_repo: ProductRepository = ProductRepository(session=session)

    async def get_all_categories(self, page: int, per_page: int) -> GetProductsResponseSchema:
        products = await self.product_repo.get_not_deleted_products(page=page, per_page=per_page)
        pages = get_pagination(
            total_items=products.total_count,
            per_page=per_page,
            page=page,
            current_items=products.current_count,
        )
        return GetProductsResponseSchema(
            products=products.products,
            pagination=pages,
        )
