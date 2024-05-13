from fastapi import APIRouter, HTTPException

from services.user_service import user_service
from schemas.user_schema import UserCreate, UserGet, UserGetWithMemberships
from schemas.status_schema import Status


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(order: str = "id", limit: int = 100, offset: int = 0) -> list[UserGetWithMemberships]:
    try:
        return user_service.get_users(order=order, limit=limit, offset=offset)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))  # type: ignore


@router.get("/user/{pk}")
def get_user_by_id(pk: int) -> UserGetWithMemberships:
    try:
        return user_service.get_user_by_id(pk=pk)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))  # type: ignore


@router.get("/user")
def get_user_by_email(email: str) -> UserGetWithMemberships:
    try:
        return user_service.get_user_by_email(email=email)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))  # type: ignore


@router.post("/create")
def create_user(data: UserCreate) -> UserGet:
    try:
        return user_service.create_user(data)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))  # type: ignore


@router.put("/{pk}/change/email")
def change_user_email(pk: int, email: str) -> UserGetWithMemberships:
    try:
        return user_service.change_user_email(pk=pk, email=email)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))  # type: ignore


@router.put("/{pk}/change/phone-number")
def change_user_phone_number(pk: int, phone_number: str) -> UserGetWithMemberships:
    try:
        return user_service.change_user_phone_number(pk=pk, phone_number=phone_number)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))  # type: ignore


@router.delete("/{pk}/delete")
def delete_user(pk: int) -> Status:
    try:
        user_service.delete_user_by_id(pk=pk)
        return Status(code=200, message="User deleted successfully")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))  # type: ignore
