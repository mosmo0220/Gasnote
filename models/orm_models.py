"""Database models for orm"""
import dataclasses
from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship
from database import Base

@dataclasses.dataclass
class User(Base):
    """ORM representation for User table"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    notebooks = relationship("Notebook", back_populates="owner")

@dataclasses.dataclass
class Notebook(Base):
    """ORM representation for Notebooks table"""
    __tablename__ = "notebooks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(JSON, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="notebooks")
