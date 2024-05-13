from repositories.membership_repository import membership_repository
from schemas.membership_schema import MembershipCreate, MembershipGet


class MembershipService:
    def create_membership(self, data: MembershipCreate) -> MembershipGet:
        return MembershipGet.model_validate(membership_repository.create(data=data))

    def get_memberships(
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

    def get_membership_by_id(self, pk: int) -> MembershipGet:
        return MembershipGet.model_validate(membership_repository.get_single(id=pk))

    def delete_membership_by_id(self, pk: int) -> None:
        membership_repository.delete(id=pk)


membership_service = MembershipService()
