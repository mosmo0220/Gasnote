"""Base case import for user auth process"""
from typing import Annotated
from fastapi import Depends
from utilities.auth import get_current_user

UserDependency = Annotated[dict, Depends(get_current_user)]
