"""
Module which contains API endpoints for RSS Feeds.
"""

from typing import List

import fastapi
import sqlalchemy as sa
import sqlalchemy.orm
from fastapi import params

from rss_reader.api import crud
from rss_reader.api import deps
from rss_reader.api import schemas
from rss_reader.workers import tasks


router = fastapi.APIRouter(
    prefix="/feeds",
    tags=["feeds"],
)


@router.get("/", response_model=List[schemas.RssFeed])
async def list_feeds(
    db: sa.orm.Session = params.Depends(deps.get_db),
    order_by: List[dict] = fastapi.Depends(deps.get_order_by_query_param),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve RSS feeds.
    """
    return crud.rss_feed.get_multiple(
        db, skip=skip, limit=limit, order_by=order_by
    )


@router.post("/", response_model=schemas.RssFeed, status_code=201)
async def create_feed(
    *,
    db: sa.orm.Session = params.Depends(deps.get_db),
    src: schemas.RssFeedCreate,
):
    """
    Create new RSS feed.
    """
    feed_obj = crud.rss_feed.create(db, create_src=src)
    tasks.fetch_feed_icon.delay(feed_obj.id)
    return feed_obj


@router.put("/{id}", response_model=schemas.RssFeed)
async def update_feed(
    *,
    db: sa.orm.Session = params.Depends(deps.get_db),
    id: int,
    src: schemas.RssFeedUpdate,
):
    """
    Update RSS feed.
    """
    feed_obj = crud.rss_feed.get(db, id=id)
    if feed_obj is None:
        raise fastapi.HTTPException(404, detail="RSS Feed not found")
    feed_obj = crud.rss_feed.update(db, obj=feed_obj, update_src=src)
    tasks.fetch_feed_icon.delay(feed_obj.id)
    return feed_obj


@router.get("/{id}", response_model=schemas.RssFeed)
async def read_feed(
    *,
    db: sa.orm.Session = params.Depends(deps.get_db),
    id: int,
):
    """
    Read RSS feed.
    """
    obj = crud.rss_feed.get(db, id=id)
    if obj is None:
        raise fastapi.HTTPException(404, detail="RSS Feed not found")
    return obj


@router.delete("/{id}", response_model=schemas.RssFeed)
async def delete_feed(
    *,
    db: sa.orm.Session = params.Depends(deps.get_db),
    id: int,
):
    """
    Delete RSS feed.
    """
    obj = crud.rss_feed.get(db, id=id)
    if obj is None:
        raise fastapi.HTTPException(404, detail="RSS Feed not found")
    return crud.rss_feed.remove(db, id=id)
