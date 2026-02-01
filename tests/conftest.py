import os

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient

load_dotenv(".test.env", override=True)

assert str(os.getenv("ENVIRONMENT")) == "TEST"

from main import create_app  # noqa


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture
async def async_client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
