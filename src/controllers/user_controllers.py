from fastapi import APIRouter, Depends

from ..services.user_service import user_service
from ..schemas.status_schemas import Status
from ..auth.schemas import UserReadWithMemberships
from ..auth.router import current_user, current_superuser

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(
    order: str = "id", limit: int = 100, offset: int = 0, user=Depends(current_superuser)
) -> list[UserReadWithMemberships]:
    return user_service.get_all(order=order, limit=limit, offset=offset)


@router.get("/me")
def get_current_user(user=Depends(current_user)) -> UserReadWithMemberships:
    return user_service.get_by_id(pk=user.id)


@router.get("/user/{pk}")
def get_user_by_id(pk: int, user=Depends(current_superuser)) -> UserReadWithMemberships:
    return user_service.get_by_id(pk=pk)


@router.get("/user")
def get_user_by_email(email: str, user=Depends(current_superuser)) -> UserReadWithMemberships:
    return user_service.get_by_email(email=email)


@router.put("/change/email")
def change_user_email(email: str, user=Depends(current_user)) -> UserReadWithMemberships:
    return user_service.change_email(pk=user.id, email=email)


@router.put("/change/phone-number")
def change_user_phone_number(phone_number: str, user=Depends(current_user)) -> UserReadWithMemberships:
    return user_service.change_phone_number(pk=user.id, phone_number=phone_number)


@router.delete("/delete")
def delete_user(user=Depends(current_user)) -> Status:
    user_service.delete_by_id(pk=user.id)
    return Status(code=200, message="User deleted successfully")
