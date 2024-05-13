from .base_schema import BaseChema


class UserCreate(BaseChema):
    first_name: str
    last_name: str
    email: str
    phone_number: str | None = None


class UserGet(UserCreate):
    id: int


class UserUpdate(BaseChema):
    pass


class UserUpdateEmail(UserUpdate):
    email: str


class UserUpdatePhoneNumber(UserUpdate):
    phone_number: str
