from schemas.service_schema import ServiceGet
from schemas.membership_schema import MembershipGet
from .base_schema import BaseChema


class OfficeCreate(BaseChema):
    address: str
    phone_number: str


class OfficeGet(OfficeCreate):
    id: int


class OfficeGetWithServices(OfficeGet):
    services: list[ServiceGet] = []


class OfficeGetWithAllRelations(OfficeGetWithServices):
    memberships: list[MembershipGet] = []


class OfficeUpdate(BaseChema):
    pass


class OfficeUpdatePhoneNumber(OfficeUpdate):
    phone_number: str
