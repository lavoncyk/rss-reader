"""
Module which contains RSS feed parser logic.
"""

from datetime import datetime
from typing import List, Optional

import celery
import celery.utils
import feedparser

from rss_reader import models
from rss_reader import utils
from rss_reader.db import session as db_session


logger = celery.utils.log.get_logger(__name__)


@celery.shared_task
def load_new_posts_from_feeds() -> None:
    """Load new posts from RSS feeds in DB."""
    db = db_session.SessionLocal()

    parse_feed_jobs = [
        parse_feed.signature((f.id, f.url, f.last_new_posts_at))
        for f in db.query(models.RssFeed).all()
    ]

    parse_jobs_group = celery.group(parse_feed_jobs)
    celery.chord(parse_jobs_group)(
        save_posts_from_feeds.signature(),
    )


@celery.shared_task
def parse_feed(
    feed_id: int,
    url: str,
    last_new_posts_at: Optional[datetime],
) -> dict:
    """Parse RSS feed.

    Args:
        feed_id (int): A feed ID in DB.
        url (str): A feed URL.
        last_new_posts_at (Optional[datetime]): A time of last new post in feed.

    Returns:
        dict: A dict representing parsed RSS feed and its posts.
    """
    parsed_feed = feedparser.parse(url, modified=last_new_posts_at)
    logger.info("Parsed %d entries from '%s' feed.",
                len(parsed_feed.entries), url)

    def str_modified_2_datetime(read_at_str: str) -> datetime:
        """Convert feed's modified date from str to datetime."""
        return datetime.strptime(read_at_str, "%a, %d %b %Y %H:%M:%S %Z")

    return {
        "rss_feed_id": feed_id,
        "read_at": str_modified_2_datetime(parsed_feed.modified),
        "posts": [
            {
                "title": entry.title,
                "url": entry.link,
                "published_at": entry.published,
                "rss_feed_id": feed_id,
            } for entry in parsed_feed.entries
        ],
    }


@celery.shared_task
def save_posts_from_feeds(feeds: List[dict]) -> None:
    """Save posts from RSS feeds in DB.

    Args:
        feeds (List[dict]): A list of parsed RSS feeds.
    """
    db = db_session.SessionLocal()

    def save_posts(feed: dict) -> dict:
        """Save posts from RSS feed."""
        db.bulk_save_objects([models.Post(**post) for post in feed["posts"]])
        logger.info("RSS feed ID = %d. Saved %d entries from feed.",
                    feed["rss_feed_id"], len(feed["posts"]), )
        return feed

    def update_read_timestamp(feed: dict) -> dict:
        """Update read timestamp of RSS feed."""
        feed_obj = db.query(models.RssFeed).get(feed["rss_feed_id"])
        feed_obj.last_new_posts_at = feed["read_at"]
        db.add(feed_obj)
        return feed

    utils.pipeline_each(
        feeds,
        [
            save_posts,
            update_read_timestamp,
        ])

    db.commit()
