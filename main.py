"""Uvicorn main module"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.orm_models import Base
from imports.auth01_router import Auth01Router
from utilities.redirects.redirect_on_401 import RedirectOn401Middleware
from database import engine

from routes.auth.auth_router import AuthRoutes
from routes.website.website_router import WebsiteRoutes

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(WebsiteRoutes)
app.include_router(Auth01Router)
app.include_router(AuthRoutes)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(RedirectOn401Middleware)

templates = Jinja2Templates(directory="templates")

@app.get("/login")
async def login(request: Request):
    """Website route to render login page"""
    return templates.TemplateResponse("/auth/login.html", {"request": request})

@app.get("/register")
async def register(request: Request):
    """Website route to render register page"""
    return templates.TemplateResponse("/auth/register.html", {"request": request})
