"""Script which loads initial data."""

from typing import Set, Type, Union

import logging
import os
import yaml

import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader import models
from rss_reader.db import session


BASE_DIR = os.path.join(os.path.dirname(__file__), "..")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("init_data")


def _load_data() -> Union[dict, list, None]:
    """Load initial data from file."""
    data_file_path = os.path.join(BASE_DIR, "feeds.yaml")
    with open(data_file_path) as file:
        try:
            data = yaml.load(file.read(), Loader=yaml.FullLoader)
        except yaml.YAMLError as err:
            logger.error("Invalid YAML file: '%s': %s", data_file_path, err)
            exit(1)
    return data


def _get_or_create_category(
    db: sa.orm.Session, category_data: dict
) -> models.Category:
    """Get existing Category object from DB or create one."""
    category_obj = (
        db.query(models.Category)
        .filter(models.Category.slug == category_data["slug"])
        .first()
    )
    if category_obj is None:
        category_obj = models.Category()
        logger.info("Creating category '%s'", category_data["slug"])

    category_obj.slug = category_data["slug"]
    category_obj.name = category_data["name"]

    db.add(category_obj)
    return category_obj


def _get_or_create_feed(
    db: sa.orm.Session, feed_data: dict, category: models.Category
) -> models.RssFeed:
    """Get existing RssFeed object from DB or create one."""
    feed_obj = (
        db.query(models.RssFeed)
        .filter(models.RssFeed.url == feed_data["url"])
        .first()
    )
    if feed_obj is None:
        feed_obj = models.RssFeed()
        logger.info("Creating feed '%s'", feed_data["url"])

    feed_obj.name = feed_data["name"]
    feed_obj.url = feed_data["url"]
    feed_obj.category = category

    db.add(feed_obj)
    return feed_obj


def _delete_objects(
    db: sa.orm.Session, model: Type[models.Base], exclude_ids: Set[int]
) -> None:
    """Delete objects except ones which IDs provided."""
    objs_to_remove = db.query(model).filter(model.id.not_in(exclude_ids)).all()
    if objs_to_remove:
        ids = [o.id for o in objs_to_remove]
        logger.info("Removing %s objects with IDs: %s", model.__name__, ids)
        db.query(model).filter(model.id.in_(ids)).delete()


def init_data():

    logger.info("Init data")

    data = _load_data()
    db = session.SessionLocal()

    category_ids = set()
    feed_ids = set()
    for category_data in (data.get("categories") or []):
        category_obj = _get_or_create_category(db, category_data)
        category_ids.add(category_obj.id)
        for feed_data in (category_data.get("feeds") or []):
            feed_obj = _get_or_create_feed(db, feed_data, category_obj)
            feed_ids.add(feed_obj.id)
        db.flush()

    _delete_objects(db, models.RssFeed, exclude_ids=feed_ids)
    _delete_objects(db, models.Category, exclude_ids=category_ids)

    db.commit()


if __name__ == "__main__":
    init_data()
