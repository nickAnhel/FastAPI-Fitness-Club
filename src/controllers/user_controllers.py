from fastapi import APIRouter

from ..services.user_service import user_service
from ..schemas.user_schema import UserCreate, UserGet, UserGetWithMemberships
from ..schemas.status_schema import Status


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(order: str = "id", limit: int = 100, offset: int = 0) -> list[UserGetWithMemberships]:
    return user_service.get_all(order=order, limit=limit, offset=offset)


@router.get("/user/{pk}")
def get_user_by_id(pk: int) -> UserGetWithMemberships:
    return user_service.get_by_id(pk=pk)


@router.get("/user")
def get_user_by_email(email: str) -> UserGetWithMemberships:
    return user_service.get_by_email(email=email)


@router.post("/create")
def create_user(data: UserCreate) -> UserGet:
    return user_service.create(data)


@router.put("/{pk}/change/email")
def change_user_email(pk: int, email: str) -> UserGetWithMemberships:
    return user_service.change_email(pk=pk, email=email)


@router.put("/{pk}/change/phone-number")
def change_user_phone_number(pk: int, phone_number: str) -> UserGetWithMemberships:
    return user_service.change_phone_number(pk=pk, phone_number=phone_number)


@router.delete("/{pk}/delete")
def delete_user(pk: int) -> Status:
    user_service.delete_by_id(pk=pk)
    return Status(code=200, message="User deleted successfully")
