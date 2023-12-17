"""Notebook crud opperation on Database"""
from sqlalchemy.orm import Session

import models.orm_models as models
import models.pydantic_models as schemas

def get_notebooks(db: Session, user_id: int):
    """Request to db for all user notebooks"""
    return db.query(models.Notebook).filter(models.Notebook.owner_id == user_id).all()

def create_user_notebook(db: Session, item: schemas.NotebookCreate, user_id: int):
    """Request to db that add new notebook"""
    db_item = models.Notebook(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Add update funtion
# Add delete funtion
