"""API Router for website routes"""
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from imports.user_dependency import UserDependency

WebsiteRoutes = APIRouter(
    prefix='/app',
    tags=['website']
)

templates = Jinja2Templates(directory="templates")

@WebsiteRoutes.get("/")
# pylint: disable=W0613
async def index(request: Request, user: UserDependency):
    """Returns Jinja2 page, that is main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@WebsiteRoutes.get("/status")
# pylint: disable=W0613
async def validate_credentials(user: UserDependency):
    """Returns Jinja2 page, that checks auth system"""
    return RedirectResponse("/app", status_code=200)

@WebsiteRoutes.get("/engine-load")
async def load_engine(request: Request):
    """Returns Jinja2 page, that loads engine"""
    return templates.TemplateResponse("engine.html", {"request": request})
