"""
Module with the API dependencies.
"""

from typing import Generator

import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader.db import session


def get_db() -> Generator[sa.orm.Session, None, None]:
    """
    Get DB session instance.
    """
    try:
        db = session.SessionLocal()
        yield db
    finally:
        db.close()
