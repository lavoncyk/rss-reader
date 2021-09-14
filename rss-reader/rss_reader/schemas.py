"""
Module which contains API schema definition.
"""

from typing import Optional

import pydantic
from pydantic.networks import HttpUrl


class RssFeedBase(pydantic.BaseModel):
    """
    Base RSS Feed model.
    """
    name: Optional[str] = None
    url: Optional[HttpUrl] = None


class RssFeedCreate(RssFeedBase):
    """
    Model used for RSS feed creation.
    """
    name: str
    url: HttpUrl


class RssFeedUpdate(RssFeedBase):
    """
    Model used for RSS feed update.
    """


class RssFeed(RssFeedBase):
    """
    Model used for RSS feed representation.
    """
    id: int
    name: str
    url: HttpUrl

    class Config:
        orm_mode = True
