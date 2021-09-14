"""
Module which contains RSS Feed CRUD operations.
"""

from rss_reader.crud import base
from rss_reader import models
from rss_reader import schemas


class CrudRssFeed(
    base.CrudBase[models.RssFeed, schemas.RssFeedCreate, schemas.RssFeedUpdate],
):
    """
    RSS Feed CRUD class.
    """


rss_feed = CrudRssFeed(models.RssFeed)
