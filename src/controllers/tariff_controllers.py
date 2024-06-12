from fastapi import APIRouter, Depends

from ..services.tariff_service import tariff_service
from ..schemas.status_schemas import Status
from ..schemas.tariff_schemas import TariffCreate, TariffGet
from ..auth.router import current_superuser


router = APIRouter(prefix="/tariffs", tags=["tariffs"])


@router.get("/")
def get_tariffs(order: str = "id", limit: int = 100, offset: int = 0) -> list[TariffGet]:
    return tariff_service.get_all(order=order, limit=limit, offset=offset)


@router.get("/tariff/{pk}")
def get_tariff_by_id(pk: int, user=Depends(current_superuser)) -> TariffGet:
    return tariff_service.get_by_id(pk=pk)


@router.post("/create")
def create_tariff(data: TariffCreate, user=Depends(current_superuser)) -> TariffGet:
    return tariff_service.create(data=data)


@router.delete("/{pk}/delete")
def delete_tariff_by_id(pk: int, user=Depends(current_superuser)) -> Status:
    tariff_service.delete_by_id(pk=pk)
    return Status(code=200, message="Service deleted successfully")
