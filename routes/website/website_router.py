"""API Router for website routes"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from models.utilities.OAuth.imports.user_dependency import UserDependency

WebsiteRoutes = APIRouter(
    prefix='/app',
    tags=['website']
)

templates = Jinja2Templates(directory="templates")

@WebsiteRoutes.get("/")
async def index(request: Request):
    """Returns Jinja2 page, that is main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@WebsiteRoutes.get("/tryauth")
async def tryauth(user: UserDependency, request: Request):
    """Returns Jinja2 page, that checks auth system"""
    return templates.TemplateResponse("tryauth.html",
                                     {"request": request, "email": user.get("username")})

# Add /app/login
