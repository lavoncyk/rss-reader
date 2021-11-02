"""
Module with the Rss Feed model.
"""

import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader.models import base
from rss_reader.models import mixins


class RssFeed(mixins.WithCreatedAt, base.Base):
    """
    Rss Feed model.
    """
    name = sa.Column(sa.String(255), nullable=False)
    url = sa.Column(sa.Text, nullable=False)
    parsed_at = sa.Column(sa.DateTime, nullable=True)
    modified_at = sa.Column(sa.DateTime, nullable=True)
    etag = sa.Column(sa.Text, nullable=True)

    category_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("categories.id"),
        nullable=True,
    )

    category = sa.orm.relationship("Category", backref="feeds")
