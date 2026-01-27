from .categories import categories_router
from .health import health_router
from .products import router as products_router

__all__ = [
    "categories_router",
    "health_router",
    "products_router",
]
