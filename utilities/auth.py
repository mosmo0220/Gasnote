"""Standart Auth module. Do not import in any other files"""
from typing import Annotated
from datetime import timedelta, datetime

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError

import models.models as schemas
from utilities.users_operations import get_user_by_email
from utilities.token_refresh_operations import get_token_refresh_rate, \
    create_token_count, update_token_count
from database import get_db
from load_env import SECRET_KEY, ALG

router = APIRouter(
    prefix='/auth/01',
    tags=['auth01']
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES = 60

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/01/token')

class Token(BaseModel):
    """Base model for Token"""
    access_token: str
    token_type: str

def authenticate_user(email: str, password: str, db):
    """Function chceks if user provide correct password"""
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(email: str, user_id: int, expires_delta: timedelta, db):
    """Function creates JWT Token"""
    # Add time checking for DDOS attack
    encode = {'sub': email, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})

    token_count = get_token_refresh_rate(db, user_id)

    if token_count is None:
        create_token_count(db, refresh_token=schemas.RefreshTokenCreate(user_id=user_id))
    elif token_count.refresh_count == 0:
        update_token_count(db, user_id=user_id, count=1)

    return jwt.encode(encode, SECRET_KEY, ALG)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """Function finalize token checking"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALG])
        email: str = payload.get('sub')
        user_id: int = payload.get('id')

        if email is None or user_id is None:
            return RedirectResponse("/app/login", status_code=401)
        return {'username': email, 'id': user_id}
    except JWTError:
        return RedirectResponse("/app/login", status_code=401)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                db: Annotated[Session, Depends(get_db)]) -> Token:
    """Function finalize user auth process"""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return RedirectResponse("/app/login", status_code=401)
    token = create_access_token(user.email, user.id,
                               timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), db)

    return {'access_token': token, 'token_type': 'bearer'}

@router.post("/token/refresh", response_model=Token)
async def refresh_token(user: Annotated[dict, Depends(get_current_user)],
                       db: Annotated[Session, Depends(get_db)]) -> Token:
    """Function allows to refresh user token"""
    # Add time checking for DDOS attack
    token_count = get_token_refresh_rate(db, user.get("id"))
    if token_count.refresh_count >= 24 or token_count.refresh_count == 0:
        update_token_count(db, user.get("id"), 0)
        return RedirectResponse("/app/login", status_code=301)

    counter = token_count.refresh_count
    update_token_count(db, user.get("id"), counter + 1)
    access_token_expires = timedelta(minutes=REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(user.get("sub"), user.get("id"), access_token_expires, db)
    return {'access_token': token, 'token_type': 'bearer'}
