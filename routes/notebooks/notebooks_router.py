"""API Router for notebooks"""
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette import status

from sqlalchemy.orm import Session

import models.pd_models as schemas
from utilities.operations.notebooks_operations import \
    get_notebook as models_get_notebook, create_user_notebook as models_create_user_notebook, \
    update_user_notebook as models_update_user_notebook, \
    delete_user_notebook as models_delete_user_notebook
from imports.user_dependency import UserDependency
from database import get_db

NotebooksRoutes = APIRouter(
    prefix="/notebooks",
    tags=['notebooks']
)

@NotebooksRoutes.get("/get")
# pylint: disable=W0613
async def get_notebook(user: UserDependency, notebook_id: int,
                      db: Annotated[Session, Depends(get_db)]):
    """API route to get user notebook"""
    result = models_get_notebook(db, notebook_id)
    return_notebook = result.model_dump_json()
    return JSONResponse(return_notebook)


@NotebooksRoutes.post("/create", status_code=status.HTTP_201_CREATED)
async def create_notebook(user: UserDependency, notebook: schemas.NotebookCreate,
                         db: Annotated[Session, Depends(get_db)]):
    """API route to create new notebook"""
    print(notebook)
    return models_create_user_notebook(db, notebook, user.get("id"))

@NotebooksRoutes.patch("/update")
# pylint: disable=W0613
async def update_notebook(user: UserDependency, updated_notebook: schemas.Notebook,
                         db: Annotated[Session, Depends(get_db)]):
    """API route to update user notebook"""
    return models_update_user_notebook(db, updated_notebook.id, updated_notebook.title,
                                      updated_notebook.content)

@NotebooksRoutes.delete("/delete")
# pylint: disable=W0613
async def delete_notebook(user: UserDependency, notebook_id: int,
                         db: Annotated[Session, Depends(get_db)]):
    """API route to delete user notebook"""
    return models_delete_user_notebook(db, notebook_id)
