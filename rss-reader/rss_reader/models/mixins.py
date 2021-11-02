"""
Module with common mixins.
"""

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext import declarative


class WithCreatedAt:
    """
    Mixin which adds created at timestamp.
    """
    @declarative.declared_attr
    def created_at(cls):
        return sa.Column(
            sa.DateTime,
            nullable=False,
            default=lambda: datetime.utcnow().replace(microsecond=0),
        )
