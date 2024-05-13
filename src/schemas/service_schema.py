from pydantic import BaseModel

from models.models import ServiceType


class ServiceBase(BaseModel):
    class Config:
        from_attributes = True


class ServiceCreate(ServiceBase):
    service_type: ServiceType


class ServiceGet(ServiceCreate):
    id: int
