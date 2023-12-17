"""User crud opperation on Database"""
from sqlalchemy.orm import Session

import models.orm_models as models
import models.pydantic_models as schemas

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
    # Add hashing function!
    hashed_password = user.password

    # pylint: disable=E1123
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Add update funtion
# Add delete funtion
