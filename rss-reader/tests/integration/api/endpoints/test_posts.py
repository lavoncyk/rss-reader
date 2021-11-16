"""
Tests for /posts endpoints.
"""

from fastapi import testclient
import sqlalchemy as sa
import sqlalchemy.orm

from tests.integration import factories
from tests.integration import utils


def test_read_post(
    client: testclient.TestClient, db_session: sa.orm.Session
):
    """
    Test read post.
    """
    post = factories.PostFactory()

    response = client.get(f"/api/posts/{post.id}/")

    assert response.status_code == 200
    content = response.json()
    utils.assert_obj_payload(
        payload=content,
        exp_payload={
            "id": post.id,
            "rss_feed_id": post.rss_feed_id,
            "title": post.title,
            "url": post.url,
            "published_at": post.published_at,
            "is_new": post.is_new,
        })


def test_read_post_not_exist(
    client: testclient.TestClient, db_session: sa.orm.Session
):
    """
    Test read not existing post returns 404.
    """
    post = factories.PostFactory()
    non_existing_feed_id = post.id + 1

    response = client.get(f"/api/posts/{non_existing_feed_id}/")

    assert response.status_code == 404
    content = response.json()
    utils.assert_err_detail(payload=content, exp_detail="Post not found")


def test_list_posts(
    client: testclient.TestClient, db_session: sa.orm.Session,
):
    """
    Test list posts.
    """
    with factories.single_commit(db_session):
        factories.PostFactory()
        factories.PostFactory()

    response = client.get("/api/posts/")

    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2


def test_list_posts_of_feed(
    client: testclient.TestClient, db_session: sa.orm.Session,
):
    """
    Test list posts of a specific RSS feed.
    """
    with factories.single_commit(db_session):
        post_1 = factories.PostFactory()
        factories.PostFactory()

    response = client.get(f"/api/feeds/{post_1.rss_feed_id}/posts/")

    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
