"""
Module which contains API endpoints for Posts.
"""

from typing import List

import fastapi
import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader.api import crud
from rss_reader.api import deps
from rss_reader.api import schemas
from rss_reader.config import settings


router = fastapi.APIRouter(
    tags=["posts"],
)


@router.get("/posts/", response_model=List[schemas.Post])
async def read_posts(
    db: sa.orm.Session = fastapi.Depends(deps.get_db),
    cache_control: deps.CacheControl = fastapi.Depends(),
    order_by: List[dict] = fastapi.Depends(deps.get_order_by_query_param),
    skip: int = 0,
    limit: int = 100,
):
    """
    List posts.
    """
    cache_control.set(f"max-age: {settings.RSS_PARSE_FEEDS_INTERVAL}, public")
    return crud.post.get_multiple(db, skip=skip, limit=limit, order_by=order_by)


@router.get("/posts/{id}", response_model=schemas.Post)
async def read_post(
    *,
    db: sa.orm.Session = fastapi.Depends(deps.get_db),
    cache_control: deps.CacheControl = fastapi.Depends(),
    id: int,
):
    """
    Get post.
    """
    cache_control.set(f"max-age: {settings.RSS_PARSE_FEEDS_INTERVAL}, public")
    obj = crud.post.get(db, id=id)
    if obj is None:
        raise fastapi.HTTPException(404, detail="Post not found")
    return obj


@router.get("/feeds/{id}/posts", response_model=List[schemas.Post])
async def read_feed_posts(
    *,
    db: sa.orm.Session = fastapi.Depends(deps.get_db),
    cache_control: deps.CacheControl = fastapi.Depends(),
    order_by: List[dict] = fastapi.Depends(deps.get_order_by_query_param),
    id: int,
    skip: int = 0,
    limit: int = 100,
):
    """
    List posts related to RSS feed.
    """
    cache_control.set(f"max-age: {settings.RSS_PARSE_FEEDS_INTERVAL}, public")
    obj = crud.rss_feed.get(db, id=id)
    if obj is None:
        raise fastapi.HTTPException(404, detail="RSS Feed not found")
    return crud.post.get_multiple_by_feed(
        db,
        feed_id=id,
        skip=skip,
        limit=limit,
        order_by=order_by,
    )
