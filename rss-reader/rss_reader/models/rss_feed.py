"""
Module with the Rss Feed model.
"""

import sqlalchemy as sa
from sqlalchemy.sql.expression import null

from rss_reader.models import base


class RssFeed(base.Base):
    """
    Rss Feed model.
    """
    name = sa.Column(sa.String(255), nullable=False)
    url = sa.Column(sa.Text, nullable=False)
