from pathlib import Path
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from ..controllers.office_controllers import get_offices, get_office_by_id


BASE_DIR = Path(__file__).resolve().parent.parent


router = APIRouter(
    prefix="/pages",
    tags=["pages"],
)

templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))


@router.get("/")
def get_home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/offices")
def get_offices_page(request: Request, offices=Depends(get_offices)):
    return templates.TemplateResponse("offices.html", {"request": request, "offices": offices})


@router.get("/offices/{pk}")
def get_office_page(request: Request, office=Depends(get_office_by_id)):
    return templates.TemplateResponse("office.html", {"request": request, "office": office})
