from fastapi import APIRouter


router = APIRouter(prefix="/offices", tags=["offices"])


@router.get("/")
def get_offices():
    return [None]
