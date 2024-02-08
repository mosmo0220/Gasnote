"""User crud opperation on Database"""
from sqlalchemy.orm import Session

import models.orm_models as models
import models.pydantic_models as schemas

from models.utilities.OAuth.imports.bcrypt_context import crypt_context

def get_user(db: Session, user_id: int):
    """Request to db for user by id"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Request to db for user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Request to db for all users"""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """Request to db that add new user"""
    hashed_password = crypt_context.hash(user.password)

    # pylint: disable=E1123
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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
