"""
Module which contains User CRUD operations.
"""
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader import models
from rss_reader import security
from rss_reader.api import schemas
from rss_reader.api.crud import base


class CrudUser(
    base.CrudBase[models.User, schemas.UserCreate, schemas.UserUpdate],
):
    """
    User CRUD class.
    """

    @staticmethod
    def get_by_email(
        db: sa.orm.Session, *, email: str
    ) -> Optional[models.User]:
        """Get user by email.

        Args:
            db (sa.orm.Session): A DB instance.
            email (str): A user email.

        Returns:
            Optional[models.User]: A user or None.
        """
        return db.query(models.User).filter(models.User.email == email).first()

    def create(
        self, db: sa.orm.Session, *, create_src: schemas.UserCreate
    ) -> models.User:
        """Create a user.

        Args:
            db (sa.orm.Session): A DB instance.
            create_src (schemas.UserCreate): Data used to create a user.

        Returns:
            models.User: Created user.
        """
        user_obj = models.User()
        user_obj.email = create_src.email
        user_obj.password = security.get_password_hash(create_src.password)
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj


user = CrudUser(models.User)
