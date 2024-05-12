from fastapi import APIRouter
from controllers import (
    memberships,
    offices,
    services,
    users,
)


def get_routers() -> list[APIRouter]:
    return [
        memberships.router,
        offices.router,
        services.router,
        users.router,
    ]
