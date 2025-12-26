import uvicorn
from fastapi import FastAPI

from shop_app.routers import health_router

app = FastAPI(
    title="Pet Project",
    description="API for Pet Project",
    version="1.0.0"
)

# кастомные middleware


# routers

app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
