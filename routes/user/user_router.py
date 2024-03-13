"""API Router for user operations"""
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from utilities.operations.users_operations import \
    get_user_by_email as models_get_user_by_email, \
    update_user as models_update_user
from imports.user_dependency import UserDependency
from database import get_db

UserRoutes = APIRouter(
    prefix="/user",
    tags=['user']
)

@UserRoutes.get("/get_by_email")
# pylint: disable=W0613
async def get_user_by_email(user: UserDependency, user_email: str,
                            db: Annotated[Session, Depends(get_db)]):
    """API route to get user by email"""
    result = models_get_user_by_email(db, user_email)
    return_user = result.model_dump_json()
    return JSONResponse(return_user)

@UserRoutes.patch("/update")
async def update_user(user: UserDependency, db: Annotated[Session, Depends(get_db)],
                      new_email: str = None, new_password: str = None):
    """API route to update user data in database"""
    return models_update_user(db, user.get("id"), new_email, new_password)
