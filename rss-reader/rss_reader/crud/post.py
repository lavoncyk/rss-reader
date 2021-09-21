"""
Module which contains Post CRUD operations.
"""

from rss_reader.crud import base
from rss_reader import models
from rss_reader import schemas


class CrudPost(
    base.CrudBase[models.Post, schemas.PostCreate, schemas.PostUpdate],
):
    """
    Post CRUD class.
    """


post = CrudPost(models.Post)
