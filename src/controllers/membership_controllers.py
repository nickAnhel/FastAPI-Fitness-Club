from fastapi import APIRouter

from services.membership_service import membership_service
from schemas.membership_schema import MembershipCreate, MembershipGet
from schemas.status_schema import Status

router = APIRouter(prefix="/memberships", tags=["memberships"])


@router.get("/")
def get_memberships(order: str = "id", limit: int = 100, offset: int = 0) -> list[MembershipGet]:
    return membership_service.get_memberships(order=order, limit=limit, offset=offset)


@router.get("/membership/{pk}")
def get_membership_by_id(pk: int) -> MembershipGet:
    return membership_service.get_membership_by_id(pk=pk)


@router.post("/create")
def create_membership(data: MembershipCreate) -> MembershipGet:
    return membership_service.create_membership(data=data)


@router.delete("/delete/{pk}")
def delete_membership_by_id(pk: int) -> Status:
    membership_service.delete_membership_by_id(pk=pk)
    return Status(code=200, message="Membership deleted successfully")
