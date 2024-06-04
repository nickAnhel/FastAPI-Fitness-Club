from ..repositories.membership_repository import membership_repository
from ..schemas.membership_schemas import MembershipCreateWithPeriod, MembershipGet
from .base_service import BaseService

class MembershipService(BaseService):
    def create(self, data: MembershipCreateWithPeriod) -> MembershipGet:
        return MembershipGet.model_validate(membership_repository.create(data=data))

    def get_all(
        self,
        *,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ) -> list[MembershipGet]:
        return [
            MembershipGet.model_validate(membership)
            for membership in membership_repository.get_all(order=order, limit=limit, offset=offset)
        ]

    def get_by_id(self, pk: int) -> MembershipGet:
        return MembershipGet.model_validate(membership_repository.get_single(id=pk))

    def delete_by_id(self, pk: int) -> None:
        membership_repository.delete(id=pk)


membership_service = MembershipService()
