"""
Module which contains API schema definition for Categories.
"""

from datetime import datetime

import pydantic


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
