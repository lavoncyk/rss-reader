"""
Module with the task for loading feeds updates.
"""

from typing import List, Optional
from datetime import datetime
from datetime import timedelta
import functools

import celery.utils
import feedparser
import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader import models
from rss_reader import utils
from rss_reader.workers.app import app
from rss_reader.workers.tasks import base
from rss_reader.workers.tasks import exceptions
from rss_reader.workers.tasks import utils as task_utils


logger = celery.utils.log.get_logger(__name__)


@app.task(base=base.DatabaseTask)
def load_feeds_updates() -> None:
    """Load updates from feeds in DB."""
    db: sa.orm.Session = load_feeds_updates.db

    parse_feed_jobs = [
        parse_feed.s(
            feed_id=f.id,
            url=f.rss,
            prev_parsed_at=f.parsed_at,
            modified_at=f.modified_at,
            etag=f.etag,
        )
        for f in db.query(models.RssFeed).all()
    ]

    parse_jobs_group = celery.group(parse_feed_jobs)
    celery.chord(parse_jobs_group)(
        save_feeds_updates.signature(),
    )


@app.task
def parse_feed(
    feed_id: int,
    url: str,
    prev_parsed_at: Optional[datetime],
    modified_at: Optional[datetime],
    etag: Optional[str],
) -> Optional[task_utils.FeedStub]:
    """Parse feed.

    Args:
        feed_id (int): A feed ID in DB.
        url (str): A feed URL.
        prev_parsed_at (Optional[datetime]): A feed previously parsed timestamp.
        modified_at (Optional[datetime]): A modified time published by feed.
        etag (Optional[str]): An ETag published by feed.

    Returns:
        FeedStub: An object representing parsed feed.
    """

    # Clients should support both ETag and Last-Modified headers, as some
    # servers support one but not the other. These are needed to avoid
    # download feeds that have not changed, save bandwidth, and prevent
    # possible bans from feed publishers.
    parsed_feed = feedparser.parse(url, modified=modified_at, etag=etag)
    parsed_at = datetime.utcnow().replace(microsecond=0)

    try:
        new_posts = []
        for entry in parsed_feed["entries"]:
            post_stub = _entry_2_post(entry, feed_id)
            if _is_post_new(post_stub, prev_parsed_at):
                new_posts.append(post_stub)
    except exceptions.FeedProcessError as err:
        logger.error("Skipping feed %s due to error: %s", feed_id, err)
        new_posts = []
    else:
        logger.info(
            "Feed %d: fetched %d entries, %d new entries to be saved",
            feed_id, len(parsed_feed["entries"]), len(new_posts)
        )

    # Some feeds does not publish Last-Modified or ETag at all, which leads
    # to missing corresponding attributes, which is why `.get()` is used.
    modified = parsed_feed.get("modified_parsed")
    etag = parsed_feed.get("etag")

    return task_utils.FeedStub(
        id=feed_id,
        url=url,
        parsed_at=parsed_at,
        modified=task_utils.time_struct_2_datetime(modified),
        etag=etag,
        posts=tuple(new_posts),
    )


@app.task(base=base.DatabaseTask)
def save_feeds_updates(feeds: List[task_utils.FeedStub]) -> None:
    """Save updates from feeds in DB.

    Save posts parsed from feeds and update the feeds data in DB (i.e. update
    ETag, Last Modified, and parsed timestamp).

    Args:
        feeds (List[FeedStub]): A list of parsed feeds.
    """
    db: sa.orm.Session = save_feeds_updates.db

    save_posts = functools.partial(_save_posts, db)
    upd_feed = functools.partial(_update_feed, db)

    utils.pipeline_each(
        feeds,
        [
            save_posts,
            upd_feed,
        ])

    db.commit()


def _entry_2_post(entry: dict, feed_id: int) -> task_utils.PostStub:
    """Convert fetched entry to PostStub.

    Args:
        entry (dict): An entry fetched from feed.
        feed_id (int): A feed ID in DB.

    Returns:
        PostStub: An object representing post from RSS feed.

    Raises:
        InvalidEntry: if fetched entry contains data in unexpected format.
    """
    try:
        post_tile = entry["title"]
        post_url = entry["link"]
        post_published_at = entry["published_parsed"]
    except KeyError as err:
        logger.error(
            "The %s key is not present in parsed entry for feed %s. ",
            err, feed_id
        )
        raise exceptions.InvalidEntry from err
    return task_utils.PostStub(
        title=post_tile,
        url=post_url,
        published_at=task_utils.time_struct_2_datetime(post_published_at),
        feed_id=feed_id,
    )


def _is_post_new(
    post: task_utils.PostStub,
    prev_parsed_at: Optional[datetime],
) -> bool:
    """Check if post is new.

    Check if `post` was published after `prev_parsed_at`.

    Args:
        post (PostStub): A post to check.
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


def _save_posts(
    db: sa.orm.Session,
    feed: task_utils.FeedStub,
) -> task_utils.FeedStub:
    """Save posts from feed in DB.

    Args:
        db (sa.orm.Session): A DB session.
        feed (_RssFeedStub): An object representing parsed feed.

    Returns:
        FeedStub: An object representing parsed feed.
    """
    db.bulk_save_objects([
        models.Post(
            title=p.title,
            url=p.url,
            published_at=p.published_at,
            rss_feed_id=p.feed_id,
        ) for p in feed.posts
    ])
    return feed


def _update_feed(
    db: sa.orm.Session,
    feed: task_utils.FeedStub,
) -> task_utils.FeedStub:
    """Update parsed feed.

    Update feed's ETag, Last Modified, and parsed timestamp with actual values.

    Args:
        db (sa.orm.Session): A DB session.
        feed (FeedStub): An object representing parsed feed.

    Returns:
        FeedStub: An object representing parsed feed.
    """
    feed_obj = db.query(models.RssFeed).get(feed.id)

    feed_obj.modified_at = feed.modified
    feed_obj.etag = feed.etag
    feed_obj.parsed_at = feed.parsed_at
    feed_obj.posts_last_week = (
        db.query(models.Post)
        .filter(
            models.Post.rss_feed_id == feed.id,
            models.Post.published_at >= datetime.utcnow() - timedelta(days=7),
        )
        .count()
    )

    db.add(feed_obj)
    return feed
