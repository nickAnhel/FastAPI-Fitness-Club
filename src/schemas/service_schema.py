from models.models import ServiceType
from .base_schema import BaseChema


class ServiceCreate(BaseChema):
    service_type: ServiceType


class ServiceGet(ServiceCreate):
    id: int
