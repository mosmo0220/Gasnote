"""User crud opperation on Database"""
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models.orm_models as models
import models.pd_models as schemas

crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_user(db: Session, user_id: int) -> schemas.User:
    """Request to db for user by id"""
    result = db.query(models.User).filter(models.User.id == user_id).first()
    if result is None:
        return None
    return_user = schemas.User(email=result.email, id=result.id,
                               notebooks=result.notebooks, token_refresh=result.token_refresh)
    return return_user

def get_user_by_email(db: Session, email: str) -> schemas.User:
    """Request to db for user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Request to db for all users"""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    """Request to db that add new user"""
    hashed_password = crypt_context.hash(user.password)

    # pylint: disable=E1123
    result = models.User(email=user.email, hashed_password=hashed_password)
    db.add(result)
    db.commit()
    db.refresh(result)

    return_user = schemas.User(email=result.email, id=result.id,
                               notebooks=result.notebooks, token_refresh=0)
    return return_user

def update_user(db: Session, user_id: int, new_email: str = None, new_password: str = None):
    """Request to db to update user by user_id"""
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if user_model is None:
        return "Invalid user ID"
    if new_email is not None:
        user_model.email = new_email
    if new_password is not None:
        user_model.hashed_password = crypt_context.hash(new_password)

    db.add(user_model)
    db.commit()
    return None


def delete_user(db: Session, user_id):
    """Request to db to delete user"""
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if user_model is None:
        return "Invalid user ID"

    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return None
