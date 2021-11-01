"""
Module which contains API endpoints for Posts.
"""

from typing import List

import fastapi
import sqlalchemy as sa
import sqlalchemy.orm
from fastapi import params

from rss_reader import crud
from rss_reader import schemas
from rss_reader.api import deps


router = fastapi.APIRouter(
    tags=["posts"],
)


@router.get("/posts/", response_model=List[schemas.Post])
async def read_posts(
    db: sa.orm.Session = params.Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    List posts.
    """
    return crud.post.get_multiple(db, skip=skip, limit=limit)


@router.get("/posts/{id}", response_model=schemas.Post)
async def read_post(
    *,
    db: sa.orm.Session = params.Depends(deps.get_db),
    id: int,
):
    """
    Get post.
    """
    obj = crud.post.get(db, id=id)
    if obj is None:
        raise fastapi.HTTPException(404, detail="Post not found")
    return obj


@router.get("/feeds/{id}/posts", response_model=List[schemas.Post])
async def read_feed_posts(
    *,
    db: sa.orm.Session = params.Depends(deps.get_db),
    id: int,
    skip: int = 0,
    limit: int = 100,
):
    """
    List posts related to RSS feed.
    """
    obj = crud.rss_feed.get(db, id=id)
    if obj is None:
        raise fastapi.HTTPException(404, detail="RSS Feed not found")
    return crud.post.get_multiple_by_feed(
        db,
        feed_id=id,
        skip=skip,
        limit=limit,
    )
