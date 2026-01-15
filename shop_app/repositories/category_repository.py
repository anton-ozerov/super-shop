from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shop_app.database import Category, get_async_session
from shop_app.schemas import CategoryOut


async def get_cat_repo(session: AsyncSession = Depends(get_async_session)):  # noqa
    return CategoryRepository(session)


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_categories(self) -> list[CategoryOut] | None:
        result = await self.session.execute(select(Category))
        categories = result.scalars().all()
        if categories:
            return [CategoryOut.model_validate(cat) for cat in categories]
        return None
