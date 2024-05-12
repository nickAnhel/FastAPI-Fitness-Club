from fastapi import APIRouter


router = APIRouter(prefix="/memberships", tags=["memberships"])


@router.get("/")
def get_memberships():
    return [None]
