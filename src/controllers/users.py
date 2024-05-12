from fastapi import APIRouter, HTTPException

from repositories.user_repository import user_repository
from schemas.user_schema import UserCreate


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users():
    try:
        return user_repository.get_all()
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@router.get("/{pk}")
def get_user(pk: int):
    try:
        return user_repository.get_single(id=pk)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@router.post("/create")
def create_user(data: UserCreate):
    try:
        return user_repository.create(data.model_dump())
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@router.put("/{pk}/change/email")
def change_user_email(pk: int, email: str):
    try:
        return user_repository.update(data={"email": email}, id=pk)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@router.put("/{pk}/change/phone-number")
def change_user_phone_number(pk: int, phone_number: str):
    try:
        return user_repository.update(data={"email": phone_number}, id=pk)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@router.delete("/{pk}/delete")
def delete_user(pk: int):
    try:
        return user_repository.delete(id=pk)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
