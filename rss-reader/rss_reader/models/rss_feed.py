"""
Module with the Rss Feed model.
"""
from datetime import datetime

import sqlalchemy as sa

from rss_reader.models import base


class RssFeed(base.Base):
    """
    Rss Feed model.
    """
    name = sa.Column(sa.String(255), nullable=False)
    url = sa.Column(sa.Text, nullable=False)
    last_read_at = sa.Column(sa.DateTime, nullable=True)
    created_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=lambda: datetime.utcnow().replace(microsecond=0).isoformat(),
    )
