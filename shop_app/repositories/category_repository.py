from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shop_app.database import Category
from shop_app.schemas import CategoryOut


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_categories(self) -> list[CategoryOut] | None:
        result = await self.session.execute(select(Category))
        categories = result.scalars().all()
        if categories:
            return [CategoryOut.model_validate(cat) for cat in categories]
        return None
