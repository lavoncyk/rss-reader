"""
Module which contains base CRUD operations.
"""

from typing import Any, Generic, List, Optional, Type, TypeVar

import pydantic
import sqlalchemy as sa
from fastapi import encoders

from rss_reader.models import base as base_model


ModelType = TypeVar("ModelType", bound=base_model.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=pydantic.BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=pydantic.BaseModel)


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base CRUD class.
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
        self, db: sa.orm.Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple objects.

        Args:
            db (sa.orm.Session): A DB instance.
            skip (int, optional): Offset. Defaults to 0.
            limit (int, optional): Number of objects to fetch. Defaults to 100.

        Returns:
            List[ModelType]: List of found objects.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

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
            id (int): Oject ID.

        Returns:
            Optional[ModelType]: Deleted object or None.
        """
        obj = db.query(self.model).get(id)
        if obj is not None:
            db.delete(obj)
            db.commit()
        return obj
