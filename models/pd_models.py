"""Pydantic models"""
from pydantic import BaseModel, Json

class NotebookBase(BaseModel):
    """Base class model for Notebooks"""
    title: str
    content: Json

class NotebookCreate(NotebookBase):
    """Create object class model for Notebooks"""

class Notebook(NotebookBase):
    """Use class model for Notebooks"""
    id: int
    owner_id: int

    # pylint: disable=R0903
    class Config:
        """Pydantic config"""
        orm_mode = True

class RefreshTokenBase(BaseModel):
    """Base class model for RefreshToken"""
    user_id: int

class RefreshTokenCreate(RefreshTokenBase):
    """Create object class model for RefreshToken"""

class RefreshToken(RefreshTokenBase):
    """Use class model for RefreshToken"""
    id: int
    refresh_count: int

    # pylint: disable=R0903
    class Config:
        """Pydantic config"""
        orm_mode = True

class UserBase(BaseModel):
    """Base class model for Users"""
    email: str

class UserCreate(UserBase):
    """Create object class model for Users"""
    password: str

class User(UserBase):
    """Use class model for Users"""
    id: int
    notebooks: list[Notebook] = []
    token_refresh: RefreshToken = None

    # pylint: disable=R0903
    class Config:
        """Pydantic config"""
        orm_mode = True
