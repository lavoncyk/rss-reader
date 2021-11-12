"""
Module with the API dependencies.
"""

from typing import Generator, List, Optional
import logging

import fastapi
import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader.db import session


logger = logging.getLogger(__name__)


def get_db() -> Generator[sa.orm.Session, None, None]:
    """
    Get DB session instance.
    """
    db = session.SessionLocal()
    try:
        yield db
    except Exception:
        logger.exception("Session rollback because of exception.")
        db.rollback()
        raise
    finally:
        db.close()


class CacheControl:
    """
    Dependency which allows to configure Cache-Control.
    """
    def __init__(self, response: fastapi.Response):
        self.response = response

    def set(self, value):
        self.response.headers["Cache-Control"] = value


def get_order_by_query_param(
    order_by: Optional[str] = None,
) -> Optional[List[dict]]:
    """Get parsed order_by query parameter.

    The order_by query parameter can contain multiple comma-separated fields
    with .desc or .asc to specify an ordering: order_by=date.desc,title.asc

    Args:
        order_by (Optional[str]): An order_by query parameter. Defaults to None.

    Returns:
        Optional[List[dict]]: A list of dicts with keys "name" (the name of the
            field) and "desc" (do reverse sort if True); optional.
    """

    if order_by is None:
        return None

    order_attrs = order_by.split(",")
    parsed_order_by = []

    try:
        for order_attr in order_attrs:
            attr, order = order_attr.split(".")
            parsed_order_by.append({
                "name": attr,
                "desc": (order == "desc"),
            })
    except ValueError:
        raise fastapi.HTTPException(
            status_code=400,
            detail=f"Invalid value for 'order_by' query parameter: {order_by}"
        )

    return parsed_order_by
