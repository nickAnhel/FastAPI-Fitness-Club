from .base_schema import BaseChema
from .membership_schema import MembershipGet


class UserCreate(BaseChema):
    first_name: str
    last_name: str
    email: str
    phone_number: str | None = None


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
