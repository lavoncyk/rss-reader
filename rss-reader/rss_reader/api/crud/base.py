"""
Module which contains base CRUD operations.
"""

from typing import Any, Generic, List, Optional, Type, TypeVar

import pydantic
import sqlalchemy as sa
import sqlalchemy.orm
from fastapi import encoders

from rss_reader.models import base as base_model


ModelType = TypeVar("ModelType", bound=base_model.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=pydantic.BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=pydantic.BaseModel)


class ReadonlyCrudBase(Generic[ModelType]):
    """
    Base read-only CRUD class.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: sa.orm.Session, id: Any) -> Optional[ModelType]:
        """Get object by ID.

        Args:
            db (sa.orm.Session): A DB instance.
            id (Any): Object ID.

        Returns:
            Optional[ModelType]: Found object or None.
        """
        return db.query(self.model).get(id)

    def get_multiple(
        self,
        db: sa.orm.Session,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: List[dict] = None,
    ) -> List[ModelType]:
        """Get multiple objects.

        Args:
            db (sa.orm.Session): A DB instance.
            skip (int, optional): Offset. Defaults to 0.
            limit (int, optional): Number of objects to fetch. Defaults to 100.
            order_by (List[dict]): A list of dicts with keys "name" (the name
                of the field by which to sort) and "desc" (optional; do reverse
                sort if True).

        Returns:
            List[ModelType]: List of found objects.
        """
        query = db.query(self.model)
        query = self._apply_order_by(query, order_by)
        query = query.offset(skip).limit(limit)

        return query.all()

    def _get_order_by(self, order_by: dict) -> Any:
        """Get ORDER BY statement."""

        # transform order_by["name"] into a model's field
        attr_name = order_by["name"].lower()
        order = getattr(self.model, attr_name, None)
        if order_by.get("desc", False) and order is not None:
            order = order.desc()

        return order

    def _apply_order_by(
        self, query: sa.orm.Query, order_by: List[dict] = None
    ) -> sa.orm.Query:
        """Apply ORDER BY statements to query.

        Args:
            query (sa.orm.Query): A query.
            order_by (List[dict]): A list of dicts with keys "name" (the name
                of the field by which to sort) and "desc" (optional; do reverse
                sort if True). Defaults to None.

        Returns:
            sa.orm.Query: A query with applied ORDER BY clause.
        """
        if order_by is None:
            return query
        orders = [
            self._get_order_by(clause)
            for clause in order_by
        ]

        return query.order_by(*orders)


class CrudBase(
    ReadonlyCrudBase[ModelType],
    Generic[ModelType, CreateSchemaType, UpdateSchemaType],
):
    """
    Base CRUD class.
    """

    def create(
        self, db: sa.orm.Session, *, create_src: CreateSchemaType
    ) -> ModelType:
        """Create an object.

        Args:
            db (sa.orm.Session): A DB instance.
            create_src (CreateSchemaType): Data used to create an object.

        Returns:
            ModelType: Created object.
        """
        create_src = encoders.jsonable_encoder(create_src)
        new_obj = self.model(**create_src)
        db.add(new_obj)
        db.commit()
        db.refresh(new_obj)
        return new_obj

    def update(
        self,
        db: sa.orm.Session,
        *,
        obj: ModelType,
        update_src: UpdateSchemaType,
    ) -> ModelType:
        """Update an object.

        Args:
            db (sa.orm.Session): A DB instance.
            obj (ModelType): An object to update.
            update_src (UpdateSchemaType): Data used to update an object.

        Returns:
            ModelType: Updated object.
        """
        obj_data = encoders.jsonable_encoder(obj)
        update_src = update_src.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_src:
                setattr(obj, field, update_src[field])

        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: sa.orm.Session, *, id: Any) -> Optional[ModelType]:
        """Delete an object by ID.

        Args:
            db (sa.orm.Session): A DB instance.
            id (int): Object ID.

        Returns:
            Optional[ModelType]: Deleted object or None.
        """
        obj = db.query(self.model).get(id)
        if obj is not None:
            db.delete(obj)
            db.commit()
        return obj
