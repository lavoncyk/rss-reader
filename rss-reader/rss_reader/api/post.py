"""
Module which contains API endpoints for Posts.
"""

from typing import List

import fastapi
import sqlalchemy as sa
from fastapi import params

from rss_reader import crud
from rss_reader import schemas
from rss_reader.api import deps


router = fastapi.APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("/", response_model=List[schemas.Post])
async def read_posts(
    db: sa.orm.Session = params.Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve posts.
    """
    return crud.post.get_multiple(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Post)
async def read_post(
    *,
    db: sa.orm.Session = params.Depends(deps.get_db),
    id: int,
):
    """
    Read post.
    """
    obj = crud.post.get(db, id=id)
    if obj is None:
        raise fastapi.HTTPException(404, detail="Post not found")
    return obj
