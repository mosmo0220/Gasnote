"""API Router for user Auth"""
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from starlette import status

from sqlalchemy.orm import Session

import models.pd_models as schemas
from utilities.operations.users_operations import create_user as models_create_user, \
    get_user as models_get_user, delete_user as models_delete_user
from imports.user_dependency import UserDependency
from database import get_db

AuthRoutes = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@AuthRoutes.get("/get_user")
async def get_user(user: UserDependency, db: Annotated[Session, Depends(get_db)]):
    """API route to collect user informations"""
    result = models_get_user(db, user.get("id"))
    return_user = result.model_dump_json()
    return JSONResponse(return_user)

@AuthRoutes.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    """API route to adding new user to database"""
    return models_create_user(db, user)

@AuthRoutes.delete("/delete_user")
async def delete_user(user: UserDependency, db: Annotated[Session, Depends(get_db)]):
    """API route to delete user from database"""
    return models_delete_user(db, user.get("id"))

@AuthRoutes.get("/logout")
# pylint: disable=W0613
async def logout(user: UserDependency):
    """API route to logout user"""
    return RedirectResponse("/", 303)
