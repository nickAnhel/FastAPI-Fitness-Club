from fastapi import APIRouter, Depends

from ..services.service_service import service_service
from ..schemas.status_schemas import Status
from ..schemas.service_schemas import ServiceCreate, ServiceGet
from ..auth.router import current_superuser



router = APIRouter(prefix="/services", tags=["services"])


@router.get("/")
def get_services(order: str = "id", limit: int = 100, offset: int = 0) -> list[ServiceGet]:
    return service_service.get_all(order=order, limit=limit, offset=offset)


@router.get("/service/{pk}")
def get_service_by_id(pk: int, user=Depends(current_superuser)) -> ServiceGet:
    return service_service.get_by_id(pk=pk)


@router.post("/create/all")
def create_all_services(user=Depends(current_superuser)) -> Status:
    service_service.create_all()
    return Status(code=200, message="All services created successfully")


@router.post("/create")
def create_service(data: ServiceCreate, user=Depends(current_superuser)) -> ServiceGet:
    return service_service.create(data=data)


@router.delete("/{pk}/delete")
def delete_service_by_id(pk: int, user=Depends(current_superuser)) -> Status:
    service_service.delete_by_id(pk=pk)
    return Status(code=200, message="Service deleted successfully")
