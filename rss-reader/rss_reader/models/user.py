"""
Module with the User model.
"""

import sqlalchemy as sa

from rss_reader.models import base
from rss_reader.models import mixins


class User(mixins.WithCreatedAt, base.Base):
    """
    User model.
    """

    email = sa.Column(sa.String, unique=True, index=True, nullable=False)
    hashed_password = sa.Column(sa.String, nullable=False)
    is_active = sa.Column(sa.Boolean, default=False, nullable=False)
