from fastapi import APIRouter


router = APIRouter(prefix="/services", tags=["services"])


@router.get("/")
def get_services():
    return [None]
