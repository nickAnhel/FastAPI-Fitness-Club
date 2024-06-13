from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .config.project_config import settings
from .models.base_model import create_tables, delete_tables
from .repositories.user_repository import create_superuser
from .routes import get_routers


@asynccontextmanager
async def lifespan(application: FastAPI):
    await delete_tables()
    await create_tables()
    create_superuser()
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
