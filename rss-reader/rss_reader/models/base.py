"""
Module with the Base model.
"""

import sqlalchemy as sa


@sa.ext.declarative.as_declarative()
class Base:
    """
    Base model.
    """
    id = sa.Column(sa.Integer, primary_key=True)
