"""
Module with the DB configuration.
"""

import sqlalchemy as sa

from rss_reader.config import settings


def get_db() -> motor_async.AsyncIOMotorDatabase:
    """
    Get DB instance.
    """
    client = motor_async.AsyncIOMotorClient(settings.RSS_DB_URI)
    return client["rss_reader_db"]
