"""Rename last_read_at to last_new_posts_at for rss_feeds table

Revision ID: 02ea03a5ada0
Revises: 13387d511936
Create Date: 2021-09-24 11:34:10.460381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "02ea03a5ada0"
down_revision = "13387d511936"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "rss_feeds",
        column_name="last_read_at",
        new_column_name="last_new_posts_at",
    )


def downgrade():
    op.alter_column(
        "rss_feeds",
        column_name="last_new_posts_at",
        new_column_name="last_read_at",
    )
