from .base_schema import BaseChema
from .service_schema import ServiceGet
from .membership_schema import MembershipGet


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
