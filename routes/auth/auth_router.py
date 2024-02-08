"""API Router for user Auth"""
from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status

from sqlalchemy.orm import Session

import models.pydantic_models as schemas
from models.utilities.users_crud import create_user as models_create_user
from database import get_db

AuthRoutes = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@AuthRoutes.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    """API route to adding new user to database"""
    return models_create_user(db, user)
