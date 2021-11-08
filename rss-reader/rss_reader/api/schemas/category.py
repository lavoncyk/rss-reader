"""
Module which contains API schema definition for Categories.
"""

from typing import Optional
from datetime import datetime

import pydantic


class CategoryCreate(pydantic.BaseModel):
    """
    Model used for category creation.
    """
    name: str
    slug: str


class CategoryUpdate(pydantic.BaseModel):
    """
    Model used for category update.
    """
    name: Optional[str] = None
    slug: Optional[str] = None


class Category(pydantic.BaseModel):
    """
    Model used for Category representation.
    """

    id: int

    name: str
    slug: str

    created_at: datetime

    class Config:
        orm_mode = True


class CategoryNested(pydantic.BaseModel):
    """
    Model used for Category representation as nested schema.
    """
    id: int
    name: Optional[str]
    slug: Optional[str]
    created_at: Optional[datetime]
