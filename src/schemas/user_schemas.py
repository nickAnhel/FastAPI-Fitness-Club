from pydantic import Field

from .base_schema import BaseChema
from .membership_schemas import MembershipGet


class UserCreate(BaseChema):
    first_name: str
    last_name: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    phone_number: str | None = Field(default=None, pattern=r"^[+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$")


class UserGet(UserCreate):
    id: int


class UserGetWithMemberships(UserGet):
    memberships: list[MembershipGet]


class UserUpdate(BaseChema):
    pass


class UserUpdateEmail(UserUpdate):
    email: str


class UserUpdatePhoneNumber(UserUpdate):
    phone_number: str
