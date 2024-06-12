from fastapi import APIRouter, Depends

from ..services.membership_service import membership_service
from ..schemas.membership_schemas import MembershipCreateWithPeriod, MembershipGet
from ..schemas.status_schemas import Status
from ..auth.router import current_user, current_superuser


router = APIRouter(prefix="/memberships", tags=["memberships"])


@router.get("/")
def get_memberships(
    order: str = "id", limit: int = 100, offset: int = 0, user=Depends(current_superuser)
) -> list[MembershipGet]:
    return membership_service.get_all(order=order, limit=limit, offset=offset)


@router.get("/membership/{pk}")
def get_membership_by_id(pk: int, user=Depends(current_superuser)) -> MembershipGet:
    return membership_service.get_by_id(pk=pk)


@router.post("/create")
def create_membership(data: MembershipCreateWithPeriod, user=Depends(current_user)) -> MembershipGet:
    return membership_service.create(data=data)


@router.delete("/delete/{pk}")
def delete_membership_by_id(pk: int, user=Depends(current_user)) -> Status:
    if membership_service.delete_by_id(pk=pk, user=user):
        return Status(code=200, message="Membership deleted successfully")
    return Status(code=400, message="Membership not found")
