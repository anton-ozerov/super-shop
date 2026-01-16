import logging

import uvicorn
from fastapi import FastAPI

from shop_app.logging.config import setup_logging
from shop_app.middleware import access_log_middleware, request_id_middleware
from shop_app.routers import categories_router, health_router

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Pet Project", description="API for Pet Project", version="1.0.0")

# кастомные middleware
app.middleware("http")(access_log_middleware)
app.middleware("http")(request_id_middleware)

# routers
app.include_router(health_router)
app.include_router(categories_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
