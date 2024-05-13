from models.models import ServiceType
from repositories.office_repository import office_repository
from schemas.office_schema import OfficeCreate, OfficeGet, OfficeUpdatePhoneNumber, OfficeGetWithServices, OfficeGetWithAllRelations


class OfficeService:
    def create_office(self, data: OfficeCreate) -> OfficeGet:
        return OfficeGet.model_validate(office_repository.create(data))

    def get_offices(
        self,
        *,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ) -> list[OfficeGetWithAllRelations]:
        return [
            OfficeGetWithAllRelations.model_validate(office)
            for office in office_repository.get_all(order=order, limit=limit, offset=offset)
        ]

    def get_office_by_id(self, pk: int) -> OfficeGetWithAllRelations:
        return OfficeGetWithAllRelations.model_validate(office_repository.get_single(id=pk))

    def get_office_by_address(self, address: str) -> OfficeGetWithAllRelations:
        return OfficeGetWithAllRelations.model_validate(office_repository.get_single(address=address))

    def change_office_phone_number(self, pk: int, phone_number: str) -> OfficeGet:
        return OfficeGetWithAllRelations.model_validate(
            office_repository.update(data=OfficeUpdatePhoneNumber(phone_number=phone_number), id=pk)
        )

    def add_service_to_office(self, pk: int, service_type: ServiceType) -> OfficeGetWithServices:
        return OfficeGetWithServices.model_validate(office_repository.add_service(service_type=service_type, id=pk))

    def delete_office_by_id(self, pk: int) -> None:
        office_repository.delete(id=pk)


office_service = OfficeService()
