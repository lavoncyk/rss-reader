"""
Module with Celery app.
"""

import celery

from rss_reader.config import settings


app = celery.Celery(
    __name__,
    backend=settings.RSS_TASKS_RES_BACKEND_URI,
    broker=settings.RSS_TASKS_QUEUE_URI,
    include=[
        "rss_reader.workers.feeds_parser",
    ],
)
app.conf.timezone = "UTC"
app.conf.beat_schedule = {
    "parse-rss-feeds": {
        "task": "rss_reader.workers.feeds_parser.load_new_posts_from_feeds",
        "schedule": settings.RSS_PARSE_FEEDS_INTERVAL,
    }
}
