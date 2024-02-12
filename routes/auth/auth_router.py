"""API Router for user Auth"""
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from starlette import status

from sqlalchemy.orm import Session

import models.models as schemas
from utilities.users_operations import create_user as models_create_user
from database import get_db

AuthRoutes = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@AuthRoutes.post("/user/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    """API route to adding new user to database"""
    return models_create_user(db, user)

@AuthRoutes.get("/login")
async def login():
    """Not implemented fully"""
    return RedirectResponse("/app/", status_code=308)

@AuthRoutes.get("/logout")
async def logout():
    """Not implemented fully"""
    return RedirectResponse("/app/", status_code=308)
