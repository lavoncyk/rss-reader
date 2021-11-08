"""
Module which contains Category CRUD operations.
"""

from rss_reader.api import schemas
from rss_reader.api.crud import base
from rss_reader import models


class CrudCategory(
    base.CrudBase[
        models.Category,
        schemas.CategoryCreate,
        schemas.CategoryUpdate,
    ],
):
    """
    Category CRUD class.
    """


category = CrudCategory(models.Category)
