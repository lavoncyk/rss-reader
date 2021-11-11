"""
Model factories.
"""

import factory
import faker

from rss_reader import models


fake = faker.Faker()


class BaseModelFactory(factory.Factory):
    """
    Base model factory.
    """

    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        db = kwargs.pop("db")
        obj = model_class(*args, **kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj


class CategoryFactory(BaseModelFactory):
    """
    Category factory.
    """
    class Meta:
        model = models.Category

    name = factory.LazyAttribute(lambda x: fake.pystr())
    slug = factory.LazyAttribute(lambda x: fake.pystr())
