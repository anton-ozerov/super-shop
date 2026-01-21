from .health import health_router
from .products import router as products_router

__all__ = [
    "health_router",
    "products_router",
]
