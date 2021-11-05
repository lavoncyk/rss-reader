"""
Module with the Post model.
"""

from datetime import datetime
from datetime import timedelta

import sqlalchemy as sa
import sqlalchemy.ext.hybrid as sa_hybrid

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

    @sa_hybrid.hybrid_property
    def is_new(self) -> bool:
        """Return True if post is considered new."""
        if self.rss_feed.posts_last_week <= 1:
            delta = timedelta(days=7)
        elif self.rss_feed.posts_last_week <= 20:
            delta = timedelta(days=1)
        elif self.rss_feed.posts_last_week <= 100:
            delta = timedelta(hours=8)
        else:
            delta = timedelta(hours=4)

        now = datetime.utcnow()
        return self.published_at > now - delta
