from pydantic import BaseModel

from models.models import ServiceTypes


class ServiceBase(BaseModel):
    class Config:
        from_attributes = True


class ServiceCreate(ServiceBase):
    service_type: ServiceTypes


class ServiceGet(ServiceCreate):
    id: int
