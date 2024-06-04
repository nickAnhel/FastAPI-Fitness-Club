from fastapi_users import schemas
from pydantic import Field

from ..schemas.membership_schemas import MembershipGet


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str
    phone_number: str | None = Field(default=None, pattern=r"^[+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$")


class UserReadWithMemberships(UserRead):
    memberships: list[MembershipGet]


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    phone_number: str | None = Field(default=None, pattern=r"^[+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$")


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserUpdateEmail(UserUpdate):
    email: str


class UserUpdatePhoneNumber(UserUpdate):
    phone_number: str
