import pytest
from httpx import ASGITransport, AsyncClient

from main import create_app


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture
async def async_client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
