"""Uvicorn main module"""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from models.orm_models import Base
from models.utilities.OAuth.imports.auth01_router import Auth01Router
from database import engine

from routes.auth.auth_router import AuthRoutes
from routes.website.website_router import WebsiteRoutes

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(WebsiteRoutes)
app.include_router(Auth01Router)
app.include_router(AuthRoutes)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def redirect():
    """Redirects to app route"""
    return RedirectResponse("/app/", status_code=303)
