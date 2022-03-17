"""
Module with the API dependencies.
"""

from typing import Generator, List, Optional
import logging

import fastapi
import sqlalchemy as sa
import sqlalchemy.orm
from fastapi import security as fastapi_security
from fastapi import status
from jose import jwt

from rss_reader import models
from rss_reader import security as rss_security
from rss_reader.api import crud
from rss_reader.config import settings
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


reusable_oauth2 = fastapi_security.OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_current_user(
    db: sa.orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(reusable_oauth2),
) -> models.User:
    try:
        token_payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[rss_security.ALGORITHM]
        )
        user_id = int(token_payload["sub"])
    except (jwt.JWTError, KeyError, TypeError):
        raise fastapi.HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate token {token}",
        )
    user = crud.user.get(db, id=user_id)
    if user is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


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
