"""
Module which contains RSS feed parser logic.
"""

from datetime import datetime
from typing import List, Optional

import celery
import celery.utils
import feedparser

from rss_reader import models
from rss_reader.db import session as db_session


logger = celery.utils.log.get_logger(__name__)


@celery.shared_task
def load_new_posts_from_feeds() -> None:
    """Load new posts from RSS feeds in DB."""
    db = db_session.SessionLocal()

    parse_feed_jobs = [
        parse_feed.signature((f.id, f.url, f.last_read_at))
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
    last_read_at: Optional[datetime],
) -> dict:
    """Parse RSS feed.

    Args:
        feed_id (int): A feed ID in DB.
        url (str): A feed URL.
        last_read_at (Optional[datetime]): A time of last read of the feed.

    Returns:
        dict: A dict representing parsed RSS feed and its posts.
    """
    parsed_feed = feedparser.parse(url, modified=last_read_at)
    logger.info("Parsed %d entries from '%s' feed.",
                len(parsed_feed.entries), url)

    def str_read_at_2_datetime(read_at_str: str) -> datetime:
        """Convert feed's modified date from str to datetime."""
        return datetime.strptime(read_at_str, "%a, %d %b %Y %H:%M:%S %Z") \
                       .isoformat()

    return {
        "rss_feed_id": feed_id,
        "read_at": str_read_at_2_datetime(parsed_feed.modified),
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
def save_posts_from_feeds(feeds: List[dict]) -> int:
    """Save posts from RSS feeds in DB.

    Args:
        feeds (List[dict]): A list of parsed RSS feeds.

    Returns:
        int: A total number of saved posts.
    """
    db = db_session.SessionLocal()
    saved_posts = 0
    for feed in feeds:
        feed_obj = db.query(models.RssFeed).get(feed["rss_feed_id"])
        feed_obj.last_read_at = feed["read_at"]
        db.add(feed_obj)
        for post in feed["posts"]:
            post_obj = models.Post(**post)
            db.add(post_obj)
        saved_posts += len(feed["posts"])
    db.commit()

    logger.info("Saved %d entries from all feeds.", saved_posts)
    return saved_posts
