# ruff: disable[PT022,]
import logging

import pytest
from httpx import ASGITransport, AsyncClient

from main import create_app


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture(scope="session", autouse=True)
def test_logging():
    # Снизить уровень для явно шумных логгеров
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    # Убрать потоковые хендлеры (stdout) добавленные приложением, чтобы pytest не показывал их
    root = logging.getLogger()
    for h in list(root.handlers):
        if isinstance(h, logging.StreamHandler):
            root.removeHandler(h)

    # Добавить NullHandler и установить общий уровень WARNING
    root.addHandler(logging.NullHandler())
    root.setLevel(logging.WARNING)

    yield


@pytest.fixture
async def async_client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
