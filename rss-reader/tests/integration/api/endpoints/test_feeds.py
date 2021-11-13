"""
Tests for /feeds endpoints.
"""

from unittest import mock

from fastapi import testclient
import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader import models
from tests.integration import factories


FETCH_ICON_TASK_MOCK = mock.patch(
    "rss_reader.workers.tasks.fetch_feed_icon",
    delay=mock.Mock(return_value=None),
)


@FETCH_ICON_TASK_MOCK
def test_create_feed(
    _: mock.Mock,
    client: testclient.TestClient,
    db_session: sa.orm.Session,
    feed_payload: dict,
):
    """
    Test create feed.
    """
    response = client.post("/api/feeds/", json=feed_payload)

    assert response.status_code == 201
    content = response.json()
    assert content["name"] == feed_payload["name"]
    assert content["url"] == feed_payload["url"]
    assert content["rss"] == feed_payload["rss"]
    assert "id" in content
    feed = db_session.query(models.RssFeed).get(content["id"])
    assert feed is not None


@FETCH_ICON_TASK_MOCK
def test_create_feed_with_category(
    _: mock.Mock,
    client: testclient.TestClient,
    db_session: sa.orm.Session,
    feed_payload: dict,
):
    """
    Test create feed with category.
    """
    category = factories.CategoryFactory()
    feed_payload["category"] = {"id": category.id}

    response = client.post("/api/feeds/", json=feed_payload)

    assert response.status_code == 201
    content = response.json()
    assert content["name"] == feed_payload["name"]
    assert content["url"] == feed_payload["url"]
    assert content["rss"] == feed_payload["rss"]
    assert content["category"] is not None
    assert content["category"]["id"] == category.id
    assert "id" in content
    feed = db_session.query(models.RssFeed).get(content["id"])
    assert feed is not None


@FETCH_ICON_TASK_MOCK
def test_create_feed_with_category_not_exist(
    _: mock.Mock,
    client: testclient.TestClient,
    db_session: sa.orm.Session,
    feed_payload: dict,
):
    """
    Test create feed with category which does not exist returns 400.
    """
    category = factories.CategoryFactory()
    non_existing_category_id = category.id + 1
    feed_payload["category"] = {"id": non_existing_category_id}

    response = client.post("/api/feeds/", json=feed_payload)

    assert response.status_code == 400
    content = response.json()
    exp_message = f"Category with ID {non_existing_category_id} does not exist."
    assert content["detail"] == exp_message
    assert db_session.query(models.RssFeed).count() == 0


def test_read_feed(
    client: testclient.TestClient, db_session: sa.orm.Session
):
    """
    Test read feed.
    """
    feed = factories.RssFeedFactory()

    response = client.get(f"/api/feeds/{feed.id}/")

    assert response.status_code == 200
    content = response.json()
    assert content["name"] == feed.name
    assert content["url"] == feed.url
    assert content["rss"] == feed.rss


def test_read_feed_not_exist(
    client: testclient.TestClient, db_session: sa.orm.Session
):
    """
    Test read not existing feed returns 404.
    """
    feed = factories.RssFeedFactory()
    non_existing_feed_id = feed.id + 1

    response = client.get(f"/api/feeds/{non_existing_feed_id}/")

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "RSS Feed not found"


@FETCH_ICON_TASK_MOCK
def test_update_feed(
    _: mock.Mock,
    client: testclient.TestClient,
    db_session: sa.orm.Session,
    feed_payload: dict,
):
    """
    Test update feed.
    """
    feed = factories.RssFeedFactory()

    response = client.put(f"/api/feeds/{feed.id}", json=feed_payload)

    assert response.status_code == 200
    db_session.refresh(feed)
    content = response.json()
    assert content["name"] == feed_payload["name"] == feed.name
    assert content["url"] == feed_payload["url"] == feed.url
    assert content["rss"] == feed_payload["rss"] == feed.rss
    assert content["id"] == feed.id


@FETCH_ICON_TASK_MOCK
def test_update_feed_change_category(
    _: mock.Mock,
    client: testclient.TestClient,
    db_session: sa.orm.Session,
    feed_payload: dict,
):
    """
    Test update feed with new category.
    """
    with factories.single_commit(db_session):
        category_old = factories.CategoryFactory()
        category_new = factories.CategoryFactory()
        feed = factories.RssFeedFactory(category=category_old)
    feed_payload["category"] = {"id": category_new.id}

    response = client.put(f"/api/feeds/{feed.id}", json=feed_payload)

    assert response.status_code == 200
    db_session.refresh(feed)
    content = response.json()
    assert content["name"] == feed_payload["name"] == feed.name
    assert content["url"] == feed_payload["url"] == feed.url
    assert content["rss"] == feed_payload["rss"] == feed.rss
    assert content["category"] is not None
    assert content["category"]["id"] == category_new.id
    assert content["id"] == feed.id


@FETCH_ICON_TASK_MOCK
def test_update_category_not_exist(
    _: mock.Mock,
    client: testclient.TestClient,
    db_session: sa.orm.Session,
    feed_payload: dict,
):
    """
    Test update not existing feed returns 404.
    """
    feed = factories.RssFeedFactory()
    non_existing_feed_id = feed.id + 1

    response = client.put(
        f"/api/feeds/{non_existing_feed_id}",
        json=feed_payload,
    )

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "RSS Feed not found"


def test_delete_feed(
    client: testclient.TestClient, db_session: sa.orm.Session
):
    """
    Test delete feed.
    """
    feed = factories.RssFeedFactory()

    response = client.delete(f"/api/feeds/{feed.id}")

    db_session.expunge_all()
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == feed.name
    assert content["url"] == feed.url
    assert content["rss"] == feed.rss
    assert content["id"] == feed.id
    feed = db_session.query(models.RssFeed).get(feed.id)
    assert feed is None


def test_delete_feed_not_exist(
    client: testclient.TestClient, db_session: sa.orm.Session
):
    """
    Test delete not existing feed returns 404.
    """
    feed = factories.RssFeedFactory()
    non_existing_feed_id = feed.id + 1

    response = client.delete(f"/api/feeds/{non_existing_feed_id}")

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "RSS Feed not found"


def test_list_feeds(
    client: testclient.TestClient, db_session: sa.orm.Session,
):
    """
    Test list feeds.
    """
    with factories.single_commit(db_session):
        factories.RssFeedFactory()
        factories.RssFeedFactory()

    response = client.get("/api/feeds/")

    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2
