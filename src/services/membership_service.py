from ..repositories.membership_repository import membership_repository
from ..schemas.membership_schemas import MembershipCreateWithPeriod, MembershipGet
from ..auth.models import UserModel
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

    def delete_by_id(self, pk: int, user: UserModel) -> bool:
        for membership in user.memberships:
            if membership.id == pk:
                membership_repository.delete(id=pk)
                return True
        return False


membership_service = MembershipService()
