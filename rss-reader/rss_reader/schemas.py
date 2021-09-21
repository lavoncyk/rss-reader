"""
Module which contains API schema definition.
"""

from datetime import datetime
from typing import Optional

import pydantic
from pydantic.networks import HttpUrl


class RssFeedBase(pydantic.BaseModel):
    """
    Base RSS feed model.
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
    last_read_at: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True


class PostCreate(pydantic.BaseModel):
    """
    Model used for post creation.
    """
    rss_feed_id: int
    title: str
    url: HttpUrl
    published_at: datetime


class PostUpdate(pydantic.BaseModel):
    """
    Model used for post update.
    """


class Post(pydantic.BaseModel):
    """
    Model used for post representation.
    """
    id: int
    rss_feed_id: int
    title: str
    url: HttpUrl
    published_at: datetime

    class Config:
        orm_mode = True
