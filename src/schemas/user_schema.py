from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str | None = None

    class Config:
        from_attributes = True


class UserGet(UserCreate):
    id: int
