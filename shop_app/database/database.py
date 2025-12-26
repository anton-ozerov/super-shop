from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from shop_app.core.config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass
