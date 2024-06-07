from pathlib import Path
from fastapi import APIRouter, Request, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi_users.exceptions import UserAlreadyExists

from ..auth.schemas import UserCreate
from ..auth.manager import get_user_manager
from ..auth.config import auth_backend, get_jwt_strategy
from ..auth.router import current_user, optional_current_user
from ..controllers.office_controllers import get_offices, get_office_by_id
from .forms import UserCreateForm


router = APIRouter(
    prefix="/pages",
    tags=["pages"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))


@router.get("/")
async def get_home_page(request: Request, user=Depends(optional_current_user)):
    return templates.TemplateResponse("home.html", {"request": request, "user": user})


@router.get("/offices")
def get_offices_page(request: Request, offices=Depends(get_offices), user=Depends(optional_current_user)):
    return templates.TemplateResponse("offices.html", {"request": request, "offices": offices, "user": user})


@router.get("/offices/{pk}")
def get_office_page(request: Request, office=Depends(get_office_by_id), user=Depends(optional_current_user)):
    return templates.TemplateResponse("office.html", {"request": request, "office": office, "user": user})


@router.get("/register")
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "errors": []})


@router.post("/register")
async def register(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone_number: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    user_manager=Depends(get_user_manager),
):
    form = UserCreateForm(request)
    await form.load()
    if form.is_valid():
        try:
            # print(first_name, last_name, phone_number, email, password)
            user = await user_manager.create(
                UserCreate(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                )
            )
            print(user)
            return RedirectResponse("/pages/login", status_code=303)
        except UserAlreadyExists:
            return templates.TemplateResponse(
                "register.html", {"request": request, "errors": ["This email is already in use"]}
            )
        except Exception as e:
            return templates.TemplateResponse("register.html", {"request": request, "errors": [str(e)]})
    errors = form.errors
    return templates.TemplateResponse("register.html", {"request": request, "errors": errors})


@router.get("/login")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    user_manager=Depends(get_user_manager),
):
    user = await user_manager.authenticate(
        credentials=OAuth2PasswordRequestForm(username=email, password=password),
    )

    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "errors": ["Invalid credentials"]})

    response = await auth_backend.login(get_jwt_strategy(), user)
    return RedirectResponse("/pages/", status_code=303, headers=response.headers)


@router.get("/logout")
async def logout(request: Request, user=Depends(current_user)):
    response = await auth_backend.logout(get_jwt_strategy(), user, request.headers.get("fitness_club_auth"))  # type: ignore
    return RedirectResponse("/pages/login/", status_code=303, headers=response.headers)
