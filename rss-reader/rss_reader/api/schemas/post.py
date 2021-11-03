"""
Module which contains API schema definition for Posts.
"""

from datetime import datetime

import pydantic
from pydantic.networks import HttpUrl


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
