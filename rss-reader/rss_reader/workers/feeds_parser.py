"""
Module which contains RSS feed parser logic.
"""

import time
from datetime import datetime
from typing import List, NamedTuple, Optional, Tuple

import celery
import celery.utils
import feedparser
import sqlalchemy as sa

from rss_reader import models
from rss_reader import utils
from rss_reader.db import session as db_session


logger = celery.utils.log.get_logger(__name__)


@celery.shared_task
def load_new_posts_from_feeds() -> None:
    """Load new posts from RSS feeds in DB."""
    db = db_session.SessionLocal()

    parse_feed_jobs = [
        parse_feed.signature((f.id, f.url, f.parsed_at, f.modified_at, f.etag))
        for f in db.query(models.RssFeed).all()
    ]

    parse_jobs_group = celery.group(parse_feed_jobs)
    celery.chord(parse_jobs_group)(
        save_posts_from_feeds.signature(),
    )


class _PostStub(NamedTuple):
    """Post stub."""
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
    prev_parsed_at: Optional[datetime],
) -> bool:
    """Check if post is new.

    Check if `post` was published after `last_new_posts_at`.

    Args:
        post (_PostStub): A post to check.
        prev_parsed_at (Optional[datetime]): A datetime when last post
            was published.

    Returns:
        bool: True if post is new, False otherwise.
    """
    return (
        post.published_at > prev_parsed_at
        if prev_parsed_at is not None
        else True
    )


class _RssFeedStub(NamedTuple):
    """RSS Feed stub."""
    id: int
    url: str
    parsed_at: datetime
    modified: Optional[datetime]
    etag: Optional[str]
    posts: Tuple[_PostStub]


@celery.shared_task
def parse_feed(
    feed_id: int,
    url: str,
    prev_parsed_at: Optional[datetime],
    modified_at: Optional[datetime],
    etag: Optional[str],
) -> _RssFeedStub:
    """Parse RSS feed.

    Args:
        feed_id (int): A feed ID in DB.
        url (str): A feed URL.
        prev_parsed_at (Optional[datetime]): A feed previously parsed timestamp.
        modified_at (Optional[datetime]): A modified time published by feed.
        etag (Optional[str]): An ETag published by feed.

    Returns:
        _RssFeedStub: An object representing parsed RSS feed.
    """

    # Clients should support both ETag and Last-Modified headers, as some
    # servers support one but not the other. These are needed to avoid
    # download feeds that have not changed, save bandwidth, and prevent
    # possible bans from feed publishers.
    parsed_feed = feedparser.parse(url, modified=modified_at, etag=etag)
    parsed_at = datetime.utcnow().replace(microsecond=0)
    logger.info("'%s': Fetched %d entries", url, len(parsed_feed["entries"]))

    posts = (_entry_2_post(feed_id, e) for e in parsed_feed["entries"])
    posts = tuple(p for p in posts if _is_post_new(p, prev_parsed_at))
    logger.info("'%s': %d entries after removing the old ones", url, len(posts))

    return _RssFeedStub(
        id=feed_id,
        url=url,
        parsed_at=parsed_at,
        # Some feeds does not publish Last-Modified or ETag at all, which leads
        # to missing corresponding attributes, which is `.get()` is used here.
        modified=_time_struct_2_datetime(parsed_feed.get("modified_parsed")),
        etag=parsed_feed.get("etag"),
        posts=posts,
    )


def _save_posts(db: sa.orm.Session, feed: _RssFeedStub) -> _RssFeedStub:
    """Save posts from RSS feed in DB.

    Args:
        db (sa.orm.Session): A DB session.
        feed (_RssFeedStub): An object representing parsed RSS feed.

    Returns:
        _RssFeedStub: An object representing parsed RSS feed.
    """
    db.bulk_save_objects([models.Post(**p._asdict()) for p in feed.posts])
    return feed


def _update_last_post_at_timestamp(
    db: sa.orm.Session,
    feed: _RssFeedStub,
) -> _RssFeedStub:
    """Update last_new_posts_at timestamp of RSS feed.

    Args:
        db (sa.orm.Session): A DB session.
        feed (_RssFeedStub): An object representing parsed RSS feed.

    Returns:
        _RssFeedStub: An object representing parsed RSS feed.
    """
    feed_obj = db.query(models.RssFeed).get(feed.id)
    feed_obj.last_new_posts_at = feed.modified or datetime.utcnow()
    db.add(feed_obj)
    return feed


def _update_etag(
    db: sa.orm.Session,
    feed: _RssFeedStub,
) -> _RssFeedStub:
    """Update ETag of RSS feed.

    Args:
        db (sa.orm.Session): A DB session.
        feed (_RssFeedStub): An object representing parsed RSS feed.

    Returns:
        _RssFeedStub: An object representing parsed RSS feed.
    """
    feed_obj = db.query(models.RssFeed).get(feed.id)
    feed_obj.etag = feed.etag
    db.add(feed_obj)
    return feed


def _update_parsed_at(
    db: sa.orm.Session,
    feed: _RssFeedStub,
) -> _RssFeedStub:
    """Update parsed timestamp of RSS feed.

    Args:
        db (sa.orm.Session): A DB session.
        feed (_RssFeedStub): An object representing parsed RSS feed.

    Returns:
        _RssFeedStub: An object representing parsed RSS feed.
    """
    feed_obj = db.query(models.RssFeed).get(feed.id)
    feed_obj.parsed_at = feed.parsed_at
    db.add(feed_obj)
    return feed


@celery.shared_task
def save_posts_from_feeds(feeds: List[_RssFeedStub]) -> None:
    """Save posts from RSS feeds in DB.

    Args:
        feeds (List[_RssFeedStub]): A list of parsed RSS feeds.
    """
    db = db_session.SessionLocal()
    utils.pipeline_each(
        feeds,
        [
            lambda feed: _save_posts(db, feed),
            lambda feed: _update_last_post_at_timestamp(db, feed),
            lambda feed: _update_etag(db, feed),
            lambda feed: _update_parsed_at(db, feed),
        ])

    db.commit()
