"""
Module which contains Post CRUD operations.
"""

from typing import List

import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader.api.crud import base
from rss_reader import models


class CrudPost(
    base.ReadonlyCrudBase[models.Post],
):
    """
    Post CRUD class.
    """

    def get_multiple_by_feed(
        self,
        db: sa.orm.Session,
        *,
        feed_id: int,
        skip: int = 0,
        limit: int = 100,
        order_by: List[dict] = None,
    ) -> List[models.Post]:
        """List posts based on RSS feed.

        Args:
            db (sa.orm.Session): A DB instance.
            feed_id (int): A feed ID.
            skip (int, optional): Offset. Defaults to 0.
            limit (int, optional): Number of objects to fetch. Defaults to 100.
            order_by (List[dict]): A list of dicts with keys "name" (the name
                of the field by which to sort) and "desc" (optional; do reverse
                sort if True).

        Returns:
            List[ModelType]: List of found objects.
        """
        query = db.query(self.model).filter(models.Post.rss_feed_id == feed_id)
        query = self._apply_order_by(query, order_by)
        query = query.limit(limit).offset(skip)

        return query.all()


post = CrudPost(models.Post)
