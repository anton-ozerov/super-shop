import uvicorn
from fastapi import FastAPI


app = FastAPI(
    title="Pet Project",
    description="API for Pet Project",
    version="1.0.0"
)


# кастомные middleware


# routers


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
