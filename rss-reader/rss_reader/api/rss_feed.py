"""
Module which contains API endpoints for RSS Feeds.
"""

from typing import List

import fastapi
import sqlalchemy as sa
from fastapi import params

from rss_reader import crud
from rss_reader import schemas
from rss_reader.api import deps


router = fastapi.APIRouter(
    prefix="/feeds",
    tags=["feeds"],
)


@router.get("/", response_model=List[schemas.RssFeed])
async def read_feeds(
    db: sa.orm.Session = params.Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve RSS feeds.
    """
    return crud.rss_feed.get_multiple(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.RssFeed)
async def create_feed(
    *,
    db: sa.orm.Session = params.Depends(deps.get_db),
    src: schemas.RssFeedCreate,
):
    """
    Create new RSS feed.
    """
    return crud.rss_feed.create(db, create_src=src)


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
    obj = crud.rss_feed.get(db, id=id)
    if obj is None:
        raise fastapi.HTTPException(404, detail="RSS Feed not found")
    return crud.rss_feed.update(db, obj=obj, update_src=src)


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
