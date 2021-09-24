"""
Module with the DB session configuration.
"""

import sqlalchemy as sa

from rss_reader.config import settings


engine = sa.create_engine(settings.RSS_DB_URI, pool_pre_ping=True)
SessionLocal = sa.orm.sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
