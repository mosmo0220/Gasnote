"""Standart Auth module. Do not import in any other files"""
from typing import Annotated
from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from starlette import status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError

from models.orm_models import User as Users
from database import get_db
from load_env import SECRET_KEY, ALG

router = APIRouter(
    prefix='/auth/01',
    tags=['auth01']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/01/token')

class Token(BaseModel):
    """Base model for Token"""
    access_token: str
    token_type: str

def authenticate_user(email: str, password: str, db):
    """Function chceks if user provide correct password"""
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    """Function creates JWT Token"""
    encode = {'sub': email, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, ALG)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """Function finalize token checking"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALG])
        email: str = payload.get('sub')
        user_id: int = payload.get('id')

        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': email, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.') from JWTError

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                db: Annotated[Session, Depends(get_db)]) -> Token:
    """Function finalize user auth process"""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.email, user.id, timedelta(minutes=60))

    return {'access_token': token, 'token_type': 'bearer'}
