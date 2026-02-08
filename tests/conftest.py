import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from main import create_app
from shop_app.database.database import Base, get_async_session

TEST_DB_NAME = str(os.getenv("TEST_DB_NAME"))
TEST_DB_USER = str(os.getenv("TEST_DB_USER"))
TEST_DB_PASSWORD = str(os.getenv("TEST_DB_PASSWORD"))
TEST_DB_HOST = str(os.getenv("TEST_DB_HOST"))
TEST_DB_PORT = str(os.getenv("TEST_DB_PORT"))
TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
)


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture(scope="function")
def session_maker(test_engine):
    return async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine, session_maker):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_client(db_session, session_maker):
    app = create_app()

    async def override_get_async_session():
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_async_session

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            yield ac
    finally:
        app.dependency_overrides.clear()
