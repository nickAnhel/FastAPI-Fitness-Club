from ..repositories.tariff_repository import tariff_repository
from ..schemas.tariff_schema import TariffCreate, TariffGet
from .base_service import BaseService


class TariffService(BaseService):
    def create(self, data: TariffCreate) -> TariffGet:
        return TariffGet.model_validate(tariff_repository.create(data))

    def get_all(
        self,
        *,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ) -> list[TariffGet]:
        return [
            TariffGet.model_validate(service)
            for service in tariff_repository.get_all(order=order, limit=limit, offset=offset)
        ]

    def get_by_id(self, pk: int) -> TariffGet:
        return TariffGet.model_validate(tariff_repository.get_single(id=pk))

    def delete_by_id(self, pk: int) -> None:
        tariff_repository.delete(id=pk)


tariff_service = TariffService()
