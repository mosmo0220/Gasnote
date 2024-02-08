"""Base case import for user auth process"""
from typing import Annotated
from fastapi import Depends
from models.utilities.OAuth.auth import get_current_user

UserDependency = Annotated[dict, Depends(get_current_user)]
