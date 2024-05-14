from pydantic import BaseModel, ConfigDict


class BaseChema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
