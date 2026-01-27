import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from shop_app.logging.config import setup_logging
from shop_app.middleware import access_log_middleware, request_id_middleware
from shop_app.routers import categories_router, health_router, products_router

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa RUF029
    """Контекстный менеджер для lifespan приложения"""
    logger.info("Starting up the FastAPI application", extra={"service": "lifespan"})
    try:
        yield
    finally:
        ...
        logger.info("Shutting down the FastAPI application", extra={"service": "lifespan"})


def create_app() -> FastAPI:
    """Фабрика для создания FastAPI приложения"""
    app_ = FastAPI(
        title="Pet Project",
        description="API for Pet Project",
        version="1.0.0",
        lifespan=lifespan,
    )

    # кастомные middleware
    app_.middleware("http")(access_log_middleware)
    app_.middleware("http")(request_id_middleware)

    # routers
    app_.include_router(health_router)
    app_.include_router(products_router)
    app_.include_router(categories_router)

    return app_


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
