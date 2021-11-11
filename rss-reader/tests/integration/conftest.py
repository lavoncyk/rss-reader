"""
Module with common pytest fixtures.
"""

from typing import Generator

import fastapi
import fastapi.testclient
import pytest

from rss_reader.db import session
from rss_reader.main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    """Get test client."""
    with fastapi.testclient.TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def db() -> Generator:
    try:
        db = session.SessionLocal()
        yield db
    finally:
        db.close()
