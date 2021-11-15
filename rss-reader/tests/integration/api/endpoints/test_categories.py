"""
Tests for /categories endpoints.
"""

from fastapi import testclient
import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader import models
from tests.integration import factories
from tests.integration import utils


def test_create_category(
    client: testclient.TestClient,
    db_session: sa.orm.Session,
    category_payload: dict,
):
    """
    Test create category.
    """
    response = client.post("/api/categories/", json=category_payload)

    assert response.status_code == 201
    content = response.json()
    utils.assert_obj_payload(payload=content, exp_payload=category_payload)
    category = db_session.query(models.Category).get(content["id"])
    assert category is not None


def test_read_category(
    client: testclient.TestClient, db_session: sa.orm.Session
):
    """
    Test read category.
    """
    category = factories.CategoryFactory()

    response = client.get(f"/api/categories/{category.id}/")

    assert response.status_code == 200
    content = response.json()
    utils.assert_obj_payload(
        payload=content,
        exp_payload={
            "id": category.id,
            "name": category.name,
            "slug": category.slug,
        })


def test_read_category_not_exist(
    client: testclient.TestClient, db_session: sa.orm.Session
):
    """
    Test read not existing category returns 404.
    """
    category = factories.CategoryFactory()
    non_existing_category_id = category.id + 1

    response = client.get(f"/api/categories/{non_existing_category_id}/")

    assert response.status_code == 404
    content = response.json()
    utils.assert_err_detail(payload=content, exp_detail="Category not found")


def test_update_category(
    client: testclient.TestClient,
    db_session: sa.orm.Session,
    category_payload: dict,
):
    """
    Test update category.
    """
    category = factories.CategoryFactory()

    response = client.put(
        f"/api/categories/{category.id}",
        json=category_payload,
    )

    assert response.status_code == 200
    db_session.refresh(category)
    content = response.json()
    utils.assert_obj_payload(
        payload=content,
        exp_payload=(
            category_payload |
            {
                "id": category.id,
            }
        ))


def test_update_category_not_exist(
    client: testclient.TestClient, db_session: sa.orm.Session
):
    """
    Test update not existing category returns 404.
    """
    category = factories.CategoryFactory()
    non_existing_category_id = category.id + 1
    data = {
        "name": "category 1",
        "slug": "category-1",
    }

    response = client.put(
        f"/api/categories/{non_existing_category_id}",
        json=data,
    )

    assert response.status_code == 404
    content = response.json()
    utils.assert_err_detail(payload=content, exp_detail="Category not found")


def test_delete_category(
    client: testclient.TestClient, db_session: sa.orm.Session
):
    """
    Test delete category.
    """
    category = factories.CategoryFactory()

    response = client.delete(f"/api/categories/{category.id}")

    db_session.expunge_all()
    assert response.status_code == 200
    content = response.json()
    utils.assert_obj_payload(
        payload=content,
        exp_payload={
            "id": category.id,
            "name": category.name,
            "slug": category.slug,
        })
    category = db_session.query(models.Category).get(category.id)
    assert category is None


def test_delete_category_not_exist(
    client: testclient.TestClient, db_session: sa.orm.Session
):
    """
    Test delete not existing category returns 404.
    """
    category = factories.CategoryFactory()
    non_existing_category_id = category.id + 1

    response = client.delete(f"/api/categories/{non_existing_category_id}")

    assert response.status_code == 404
    content = response.json()
    utils.assert_err_detail(payload=content, exp_detail="Category not found")


def test_list_categories(
    client: testclient.TestClient, db_session: sa.orm.Session,
):
    """
    Test list categories.
    """
    with factories.single_commit(db_session):
        factories.CategoryFactory()
        factories.CategoryFactory()

    response = client.get("/api/categories/")

    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2
