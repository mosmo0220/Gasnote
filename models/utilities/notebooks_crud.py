"""Notebook crud opperation on Database"""
from sqlalchemy import JSON
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

def update_user_notebook(db: Session, notebook_id: int,
                         new_title: str = None, new_content: JSON = None):
    """Request to db to update notebook"""
    notebook_model = db.query(models.Notebook).filter(models.Notebook.id == notebook_id).first()
    if notebook_model is None:
        return "Invalid notebook ID"
    if new_title is not None:
        notebook_model.title = new_title
    if new_content is not None:
        notebook_model.content = new_content
    db.add(notebook_model)
    db.commit()
    return None

def delete_user_notebook(db: Session, notebook_id: int):
    """Request to db to delete notebook"""
    notebook_model = db.query(models.Notebook).filter(models.Notebook.id == notebook_id).first()
    if notebook_model is None:
        return "Invalid notebook ID"
    db.query(models.Notebook).filter(models.Notebook.id == notebook_id).delete()
    db.commit()
    return None
