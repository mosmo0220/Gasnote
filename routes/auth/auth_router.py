"""API Router for user Auth"""
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from starlette import status

from sqlalchemy.orm import Session

import models.pd_models as schemas
from utilities.operations.users_operations import create_user as models_create_user, \
    delete_user as models_delete_user, update_user as models_update_user, \
    get_user as models_get_user
from imports.user_dependency import UserDependency
from database import get_db

AuthRoutes = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@AuthRoutes.get("/user/get")
async def get_user(user: UserDependency, db: Annotated[Session, Depends(get_db)]):
    """API route to collect user informations"""
    result = models_get_user(db, user.get("id"))
    return_user = result.model_dump_json()
    return JSONResponse(return_user)

@AuthRoutes.post("/user/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    """API route to adding new user to database"""
    return models_create_user(db, user)


@AuthRoutes.patch("/user/update")
async def update_user(user: UserDependency, db: Annotated[Session, Depends(get_db)],
                      new_email: str = None, new_password: str = None):
    """API route to update user data in database"""
    return models_update_user(db, user.get("id"), new_email, new_password)

@AuthRoutes.delete("/user/delete")
async def delete_user(user: UserDependency, db: Annotated[Session, Depends(get_db)]):
    """API route to delete user from database"""
    return models_delete_user(db, user.get("id"))

@AuthRoutes.get("/logout")
# pylint: disable=W0613
async def logout(user: UserDependency):
    """API route to logout user"""
    return RedirectResponse("/", 303)
