from repositories.service_repository import service_repository
from schemas.service_schema import ServiceCreate, ServiceGet


class ServiceService:
    def create_all_services(self) -> None:
        service_repository.create_all()

    def create_service(self, data: ServiceCreate) -> ServiceGet:
        return ServiceGet.model_validate(service_repository.create(data))

    def get_services(
        self,
        *,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ) -> list[ServiceGet]:
        return [
            ServiceGet.model_validate(service)
            for service in service_repository.get_all(order=order, limit=limit, offset=offset)
        ]

    def get_service_by_id(self, pk: int) -> ServiceGet:
        return ServiceGet.model_validate(service_repository.get_single(id=pk))

    def delete_service_by_id(self, pk: int) -> None:
        service_repository.delete(id=pk)


service_service = ServiceService()
