"""
Module with the Category model.
"""

import sqlalchemy as sa

from rss_reader.models import base
from rss_reader.models import mixins


class Category(mixins.WithCreatedAt, base.Base):
    """
    Category model.
    """

    name = sa.Column(sa.String(255), nullable=False)
    slug = sa.Column(sa.String(64), nullable=False)
