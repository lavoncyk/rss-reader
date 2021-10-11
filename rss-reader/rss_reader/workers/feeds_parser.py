"""
Module which contains RSS feed parser logic.
"""

import time
from datetime import datetime
from typing import List, NamedTuple, Optional, Tuple

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
        parse_feed.signature((f.id, f.url, f.last_new_posts_at, f.etag))
        for f in db.query(models.RssFeed).all()
    ]

    parse_jobs_group = celery.group(parse_feed_jobs)
    celery.chord(parse_jobs_group)(
        save_posts_from_feeds.signature(),
    )


class _PostStub(NamedTuple):
    title: str
    url: str
    published_at: datetime
    rss_feed_id: int


def _time_struct_2_datetime(
    time_struct: Optional[time.struct_time],
) -> Optional[datetime]:
    """Convert struct_time to datetime.

    Args:
        time_struct (Optional[time.struct_time]): A time struct to convert.

    Returns:
        Optional[datetime]: A converted value.
    """
    return (
        datetime.fromtimestamp(time.mktime(time_struct))
        if time_struct is not None
        else None
    )


def _entry_2_post(rss_feed_id: int, entry: dict) -> _PostStub:
    """Convert fetched entry to _PostStub.

    Convert entry fetched from RSS feed to `_PostStub`.

    Args:
        rss_feed_id (int): A feed ID in DB.
        entry (dict): An entry fetched from RSS feed.

    Returns:
        _PostStub: An object representing post from RSS feed.
    """
    return _PostStub(
        title=entry["title"],
        url=entry["link"],
        published_at=_time_struct_2_datetime(entry["published_parsed"]),
        rss_feed_id=rss_feed_id,
    )


def _is_post_new(
    post: _PostStub,
    last_new_posts_at: Optional[datetime],
) -> bool:
    """Check if post is new.

    Check if `post` was published after `last_new_posts_at`.

    Args:
        post (_PostStub): A post to check.
        last_new_posts_at (Optional[datetime]): A datetime when last post
            was published.

    Returns:
        bool: True if post is new, False otherwise.
    """
    return (
        post.published_at > last_new_posts_at
        if last_new_posts_at is not None
        else True
    )


class _RssFeedStub(NamedTuple):
    id: int
    modified: datetime
    etag: str
    posts: Tuple[_PostStub]


@celery.shared_task
def parse_feed(
    feed_id: int,
    url: str,
    last_new_posts_at: Optional[datetime],
    etag: Optional[str],
) -> _RssFeedStub:
    """Parse RSS feed.

    Args:
        feed_id (int): A feed ID in DB.
        url (str): A feed URL.
        last_new_posts_at (Optional[datetime]): A time of last new post in feed.
        etag (Optional[str]): An ETag published by feed.

    Returns:
        _RssFeedStub: An object representing parsed RSS feed.
    """

    logger.info("Parsing feed '%s'...", url)

    # Clients should support both ETag and Last-Modified headers, as some
    # servers support one but not the other. These are needed to avoid
    # download feeds that have not changed, save bandwidth, and prevent
    # possible bans from feed publishers.
    parsed_feed = feedparser.parse(url, modified=last_new_posts_at, etag=etag)
    logger.info("> Fetched %d entries from '%s' RSS feed.",
                len(parsed_feed.entries), url)

    posts = (_entry_2_post(feed_id, e) for e in parsed_feed.entries)
    posts = tuple(p for p in posts if _is_post_new(p, last_new_posts_at))
    logger.info("> Found %d new posts among fetched entries for '%s' RSS feed",
                len(posts), url)

    return _RssFeedStub(
        id=feed_id,
        modified=_time_struct_2_datetime(parsed_feed.modified_parsed),
        etag=getattr(parsed_feed, "etag", None),
        posts=posts,
    )


@celery.shared_task
def save_posts_from_feeds(feeds: List[_RssFeedStub]) -> None:
    """Save posts from RSS feeds in DB.

    Args:
        feeds (List[_RssFeedStub]): A list of parsed RSS feeds.
    """

    logger.info("Saving posts from feeds...")

    db = db_session.SessionLocal()

    def save_posts(feed: _RssFeedStub) -> _RssFeedStub:
        """Save posts from RSS feed."""
        db.bulk_save_objects([models.Post(**p._asdict()) for p in feed.posts])
        logger.info("> RSS feed ID = %d. Saved %d posts in DB.",
                    feed.id, len(feed.posts))
        return feed

    def update_read_timestamp(feed: _RssFeedStub) -> _RssFeedStub:
        """Update read timestamp of RSS feed."""
        feed_obj = db.query(models.RssFeed).get(feed.id)
        feed_obj.last_new_posts_at = feed.modified
        db.add(feed_obj)
        logger.info("> RSS feed ID = %d. Set last_new_posts_at=%s.",
                    feed.id, feed.modified)
        return feed

    def update_etag(feed: _RssFeedStub) -> _RssFeedStub:
        """Update ETag of RSS feed."""
        feed_obj = db.query(models.RssFeed).get(feed.id)
        feed_obj.etag = feed.etag
        db.add(feed_obj)
        logger.info("> RSS feed ID = %d. Set etag=%s.",
                    feed.id, feed.etag)
        return feed

    utils.pipeline_each(
        feeds,
        [
            save_posts,
            update_read_timestamp,
            update_etag,
        ])

    db.commit()
