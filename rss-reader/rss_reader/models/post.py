"""
Module with the Post model.
"""

import sqlalchemy as sa

from rss_reader.models import base
from rss_reader.models import mixins


class Post(mixins.WithCreatedAt, base.Base):
    """
    Post model.
    """

    title = sa.Column(sa.String(255), nullable=False)
    url = sa.Column(sa.Text, nullable=False)
    published_at = sa.Column(sa.DateTime, nullable=False)
    rss_feed_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("rss_feeds.id", ondelete="CASCADE"),
        nullable=False,
    )
