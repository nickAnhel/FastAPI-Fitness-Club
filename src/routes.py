from fastapi import APIRouter

from .controllers import (
    membership_controllers,
    office_controllers,
    service_controllers,
    user_controllers,
    tariff_controllers,
)
from .pages.router import router as pages_router


def get_routers() -> list[APIRouter]:
    return [
        membership_controllers.router,
        office_controllers.router,
        service_controllers.router,
        user_controllers.router,
        tariff_controllers.router,
        pages_router,
    ]
