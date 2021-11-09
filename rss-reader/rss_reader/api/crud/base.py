"""
Module which contains base CRUD operations.
"""

from typing import Any, Generic, List, Optional, Type, TypeVar
import logging

import pydantic
import sqlalchemy as sa
import sqlalchemy.orm
from fastapi import encoders

from rss_reader.api.crud import exceptions as crud_exceptions
from rss_reader.models import base as base_model


logger = logging.getLogger(__name__)


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
        new_obj = self.model()
        for attr in create_src:
            self._set_attr(db, new_obj, attr, create_src[attr])
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

        for attr in obj_data:
            if attr in update_src:
                self._set_attr(db, obj, attr, update_src[attr])

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

    def _set_attr(
        self,
        db: sa.orm.Session,
        obj: ModelType,
        attr: str,
        value: Any,
    ) -> None:
        """Set attribute value for object.

        Args:
            db (sa.orm.Session): A DB instance.
            obj (ModelType): An object which attribute to set.
            attr (set): An attribute's name.
            value (Any): A value to set.
        """
        attr_obj = getattr(self.model, attr)
        if attr_obj.__class__ is sa.orm.attributes.InstrumentedAttribute:
            # Attribute is a normal sqlalchemy descriptor.
            value = self._get_value_for_instrumented_attr(db, attr_obj, value)

        try:
            setattr(obj, attr, value)
        except AttributeError as err:
            logger.error("Failed to set the '%s' attribute: %s", attr, err)
            raise

    @staticmethod
    def _get_value_for_instrumented_attr(
        db: sa.orm.Session,
        attr_obj: sa.orm.attributes.InstrumentedAttribute,
        value: Any,
    ) -> Any:
        """Translate value to one for an InstrumentedAttribute."""
        attr_property_cls = attr_obj.property.__class__

        if attr_property_cls is sa.orm.properties.RelationshipProperty:
            rel_class = attr_obj.property.mapper.class_
            rel_obj = db.query(rel_class).get(value["id"])
            if rel_obj is None:
                raise crud_exceptions.ObjectDoesNotExist(
                    rel_class.__name__,
                    value["id"],
                )
            return rel_obj

        return value
