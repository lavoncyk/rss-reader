"""
Module which contains API schema definition for Users.
"""

from datetime import datetime
from typing import Optional

import pydantic


class UserCreate(pydantic.BaseModel):
    """
    Model used for user creation.
    """
    email: pydantic.EmailStr
    password: str


class UserUpdate(pydantic.BaseModel):
    """
    Model used for user update.
    """
    email: Optional[pydantic.EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = True


class User(pydantic.BaseModel):
    """
    Model used for user representation.
    """
    id: int

    email: pydantic.EmailStr
    is_active: bool

    created_at: datetime

    class Config:
        orm_mode = True
