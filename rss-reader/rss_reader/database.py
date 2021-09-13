"""
Module with the DB configuration.
"""

from typing import Generator

import sqlalchemy as sa

from rss_reader.config import settings


def get_db() -> Generator[sa.orm.Session, None, None]:
    """
    Get DB instance.
    """
    engine = sa.create_engine(settings.RSS_DB_URI, pool_pre_ping=True)
    session_factory = sa.orm.sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    try:
        db = session_factory()
        yield db
    finally:
        db.close()
