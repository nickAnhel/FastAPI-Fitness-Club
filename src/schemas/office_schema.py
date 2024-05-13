from pydantic import BaseModel

from schemas.service_schema import ServiceGet


class OfficeBase(BaseModel):
    class Config:
        from_attributes = True


class OfficeCreate(OfficeBase):
    address: str
    phone_number: str


class OfficeGet(OfficeCreate):
    id: int


class OfficeGetWithServices(OfficeGet):
    services: list[ServiceGet] = []


class OfficeUpdate(BaseModel):
    class Config:
        from_attributes = True


class OfficeUpdatePhoneNumber(OfficeUpdate):
    phone_number: str
