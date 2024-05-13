from fastapi import APIRouter

from services.service_service import service_service
from schemas.status_schema import Status
from schemas.service_schema import ServiceCreate, ServiceGet


router = APIRouter(prefix="/services", tags=["services"])


@router.get("/")
def get_services(order: str = "id", limit: int = 100, offset: int = 0) -> list[ServiceGet]:
    return service_service.get_services(order=order, limit=limit, offset=offset)


@router.get("/service/{pk}")
def get_service_by_id(pk: int) -> ServiceGet:
    return service_service.get_service_by_id(pk=pk)


@router.post("/create/all")
def create_all_services() -> Status:
    service_service.create_all_services()
    return Status(code=200, message="All services created successfully")


@router.post("/create")
def create_service(data: ServiceCreate) -> ServiceGet:
    return service_service.create_service(data=data)


@router.delete("/{pk}/delete")
def delete_service_by_id(pk: int) -> Status:
    service_service.delete_service_by_id(pk=pk)
    return Status(code=200, message="Service deleted successfully")