"""Split last_new_posts_at to last_parsed_at and modified_at

Revision ID: c88375693a39
Revises: a33a0c070f87
Create Date: 2021-10-18 17:47:31.277456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c88375693a39"
down_revision = "a33a0c070f87"
branch_labels = None
depends_on = None


t_name = "rss_feeds"


def upgrade():
    op.add_column(t_name, sa.Column("modified_at", sa.DateTime, nullable=True))
    op.alter_column(
        t_name,
        column_name="last_new_posts_at",
        new_column_name="parsed_at",
    )


def downgrade():
    op.drop_column(t_name, "modified_at")
    op.alter_column(
        t_name,
        column_name="parsed_at",
        new_column_name="last_new_posts_at",
    )
