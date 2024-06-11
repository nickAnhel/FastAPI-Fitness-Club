from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from .models import UserModel
from .manager import get_user_manager
from .config import auth_backend
from .schemas import UserRead, UserCreate

fastapi_users = FastAPIUsers[UserModel, int](  # type: ignore
    get_user_manager,
    [auth_backend],
)

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(
    fastapi_users.get_auth_router(auth_backend)
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate)
)

current_user = fastapi_users.current_user()
optional_current_user = fastapi_users.current_user(optional=True)
