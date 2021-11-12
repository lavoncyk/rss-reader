"""
Module with common pytest fixtures.
"""

from typing import Generator

import fastapi
import fastapi.testclient
import pytest
import sqlalchemy as sa
import sqlalchemy.orm

from tests.integration import factories
from tests.integration.config import settings
from rss_reader import models
from rss_reader.main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    """Get test client."""
    with fastapi.testclient.TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def db_engine() -> Generator[sa.engine.Engine, None, None]:
    """Get DB engine."""
    engine = sa.create_engine(settings.RSS_DB_URI, pool_pre_ping=True)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture(scope="session")
def db_session_factory(db_engine: sa.engine.Engine) -> sa.orm.scoped_session:
    """Get DB session factory."""
    return sa.orm.scoped_session(
        sa.orm.sessionmaker(bind=db_engine, autocommit=False, autoflush=False),
    )


@pytest.fixture(scope="function")
def db_session(
    db_session_factory: sa.orm.scoped_session,
) -> Generator[sa.orm.Session, None, None]:
    """Get DB session."""
    session = db_session_factory()
    # NOTE: Register factories here since they need DB session instance.
    factories.register_factories(db_session=session)

    def clear_data() -> None:
        """Clear DB data."""
        for model in models.all_models:
            session.query(model).delete()
        session.commit()

    try:
        yield session
    finally:
        clear_data()
        session.close()
