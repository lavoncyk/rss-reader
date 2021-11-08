"""
Module which contains API endpoints for Categories.
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
    prefix="/categories",
    tags=["categories"],
)


@router.get("/", response_model=List[schemas.Category])
async def list_categories(
    db: sa.orm.Session = params.Depends(deps.get_db),
    order_by: List[dict] = fastapi.Depends(deps.get_order_by_query_param),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve categories.
    """
    return crud.category.get_multiple(
        db, skip=skip, limit=limit, order_by=order_by
    )


@router.post("/", response_model=schemas.Category)
async def create_category(
    *,
    db: sa.orm.Session = params.Depends(deps.get_db),
    src: schemas.CategoryCreate,
):
    """
    Create new category.
    """
    return crud.category.create(db, create_src=src)


@router.put("/{id}", response_model=schemas.Category)
async def update_category(
    *,
    db: sa.orm.Session = params.Depends(deps.get_db),
    id: int,
    src: schemas.CategoryUpdate,
):
    """
    Update category.
    """
    category_obj = crud.category.get(db, id=id)
    if category_obj is None:
        raise fastapi.HTTPException(404, detail="Category not found")
    return crud.category.update(db, obj=category_obj, update_src=src)


@router.get("/{id}", response_model=schemas.Category)
async def read_category(
    *,
    db: sa.orm.Session = params.Depends(deps.get_db),
    id: int,
):
    """
    Read category.
    """
    obj = crud.category.get(db, id=id)
    if obj is None:
        raise fastapi.HTTPException(404, detail="Category not found")
    return obj


@router.delete("/{id}", response_model=schemas.Category)
async def delete_category(
    *,
    db: sa.orm.Session = params.Depends(deps.get_db),
    id: int,
):
    """
    Delete category.
    """
    obj = crud.category.get(db, id=id)
    if obj is None:
        raise fastapi.HTTPException(404, detail="Category not found")
    return crud.category.remove(db, id=id)
