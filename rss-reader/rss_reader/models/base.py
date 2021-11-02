"""
Module with the Base model.
"""

import sqlalchemy as sa
from sqlalchemy.ext import declarative

from rss_reader import utils


@declarative.as_declarative()
class Base:
    """
    Base model.
    """
    id = sa.Column(sa.Integer, primary_key=True)

    @declarative.declared_attr
    def __tablename__(cls) -> str:
        tablename = f"{utils.underscore_from_camelcase(cls.__name__)}s"
        if tablename.endswith("ys"):
            tablename = f"{tablename[:-2]}ies"
        return tablename
