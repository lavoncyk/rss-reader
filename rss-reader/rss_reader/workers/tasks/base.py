"""
Module with the base tasks definition.
"""

import celery
import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader.db import session as db_session


class DatabaseTask(celery.Task):  # noqa
    """Base Task class which caches DB connection."""
    _db = None

    @property
    def db(self) -> sa.orm.Session:
        """Get DB session."""
        if self._db is None:
            self._db = db_session.SessionLocal()
        return self._db
