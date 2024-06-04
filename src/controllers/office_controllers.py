from fastapi import APIRouter

from ..services.office_service import office_service
from ..schemas.office_schemas import OfficeCreate, OfficeGet, OfficeGetWithServices, OfficeGetWithAllRelations
from ..schemas.status_schemas import Status
from ..models.models import ServiceType


router = APIRouter(prefix="/offices", tags=["offices"])


@router.get("/")
def get_offices(order: str = "id", limit: int = 100, offset: int = 0) -> list[OfficeGetWithAllRelations]:
    return office_service.get_all(order=order, limit=limit, offset=offset)


@router.get("/office/{pk}")
def get_office_by_id(pk: int) -> OfficeGetWithAllRelations:
    return office_service.get_by_id(pk=pk)


@router.get("/office")
def get_office_by_address(address: str) -> OfficeGetWithAllRelations:
    return office_service.get_by_address(address=address)


@router.post("/create")
def create_office(data: OfficeCreate) -> OfficeGet:
    return office_service.create(data=data)


@router.put("/{pk}/change/phone-number")
def change_office_phone_number(pk: int, phone_number: str) -> OfficeGet:
    return office_service.change_phone_number(pk=pk, phone_number=phone_number)


@router.put("/{pk}/add-service")
def add_service_to_office(pk: int, service_type: ServiceType) -> OfficeGetWithServices:
    return office_service.add_service_to_office(pk=pk, service_type=service_type)


@router.delete("/{pk}/delete")
def delete_office_by_id(pk: int) -> Status:
    office_service.delete_by_id(pk=pk)
    return Status(code=200, message="Office deleted successfully")
