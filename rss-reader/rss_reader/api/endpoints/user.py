"""
Module which contains API endpoints for Users.
"""

from typing import List

import fastapi
import sqlalchemy as sa
import sqlalchemy.orm
from fastapi import params

from rss_reader.api import crud
from rss_reader.api import deps
from rss_reader.api import schemas


router = fastapi.APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=List[schemas.User])
async def list_users(
    db: sa.orm.Session = params.Depends(deps.get_db),
    order_by: List[dict] = fastapi.Depends(deps.get_order_by_query_param),
    skip: int = 0,
    limit: int = 100,
):
    """
    List users.
    """
    return crud.user.get_multiple(
        db, skip=skip, limit=limit, order_by=order_by
    )


@router.post("/", response_model=schemas.User, status_code=201)
async def create_user(
    *,
    db: sa.orm.Session = params.Depends(deps.get_db),
    src: schemas.UserCreate,
):
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=src.email)
    if user is not None:
        raise fastapi.HTTPException(
            status_code=400,
            detail=f"The user {src.email} already exist",
        )
    user = crud.user.create(db, create_src=src)
    return user
