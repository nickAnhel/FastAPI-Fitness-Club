from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from config.project_config import settings
from models.base_model import create_tables, delete_tables
from routes import get_routers


@asynccontextmanager
async def lifespan(application: FastAPI):
    await delete_tables()
    await create_tables()
    yield


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG,
        description=settings.DESCRIPTION,
        lifespan=lifespan,
    )

    for router in get_routers():
        application.include_router(router)

    return application


app: FastAPI = get_application()


@app.get("/")
def root():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
