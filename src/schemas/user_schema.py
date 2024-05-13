from pydantic import BaseModel


class UserBase(BaseModel):
    class Config:
        from_attributes = True


class UserCreate(UserBase):
    first_name: str
    last_name: str
    email: str
    phone_number: str | None = None


class UserGet(UserCreate):
    id: int


class UserUpdate(UserBase):
    pass


class UserUpdateEmail(UserUpdate):
    email: str


class UserUpdatePhoneNumber(UserUpdate):
    phone_number: str
