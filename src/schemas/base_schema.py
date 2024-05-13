from pydantic import BaseModel


class BaseChema(BaseModel):
    class Config:
        from_attributes = True
