from pydantic import BaseModel


class Status(BaseModel):
    code: int = 200
    message: str | None = None
