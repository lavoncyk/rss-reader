"""
Model factories.
"""

from typing import ClassVar
import contextlib

import factory
import faker
import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader import models


fake = faker.Faker()


@contextlib.contextmanager
def single_commit(db_session: sa.orm.Session):
    """Run all factory create calls in a single commit."""
    db_session.single_commit = False
    try:
        yield
    except Exception as e:
        raise e
    else:
        db_session.commit()
    finally:
        db_session.single_commit = True


class BaseModelFactory(factory.Factory):
    """
    Base model factory.
    """

    _db_session: ClassVar[sa.orm.Session] = None

    class Meta:
        abstract = True

    @classmethod
    def register(cls, db_session: sa.orm.Session) -> None:
        """Register model factory."""
        cls._db_session = db_session

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        cls._db_session.add(obj)
        if getattr(cls._db_session, "single_commit", True):
            cls._db_session.commit()
            cls._db_session.refresh(obj)
        return obj


class CategoryFactory(BaseModelFactory):
    """
    Category factory.
    """
    class Meta:
        model = models.Category

    name = factory.LazyAttribute(lambda x: fake.pystr())
    slug = factory.LazyAttribute(lambda x: fake.pystr())


def register_factories(db_session: sa.orm.Session) -> None:
    """Register all factories"""
    CategoryFactory.register(db_session)
