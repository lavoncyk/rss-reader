"""
Module with the task for fetching feed icon.
"""

import celery.utils
import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader import models
from rss_reader import utils
from rss_reader.workers.app import app
from rss_reader.workers.tasks import base


logger = celery.utils.log.get_logger(__name__)


@app.task(base=base.DatabaseTask)
def fetch_feed_icon(feed_id: int) -> None:
    """Fetch feed icon.

    Args:
        feed_id (int): A feed ID in DB.
    """
    db: sa.orm.Session = fetch_feed_icon.db
    feed_obj = db.query(models.RssFeed).get(feed_id)
    if feed_obj is None:
        logger.info("Feed %s has been deleted, cancel icon fetching.", feed_id)
        return

    fetched_icon = utils.extract_icon_url(feed_obj.url)
    feed_obj.icon = fetched_icon
    db.add(feed_obj)

    db.commit()
