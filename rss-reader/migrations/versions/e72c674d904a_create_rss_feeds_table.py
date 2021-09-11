"""Create rss_feeds table

Revision ID: e72c674d904a
Revises:
Create Date: 2021-09-11 12:08:51.054279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e72c674d904a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "rss_feeds",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("url", sa.Text, nullable=False),
    )


def downgrade():
    op.drop_table("rss_feeds")
