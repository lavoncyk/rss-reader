"""Add ETag to RSS feeds

Revision ID: a33a0c070f87
Revises: 02ea03a5ada0
Create Date: 2021-10-09 10:45:55.674241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a33a0c070f87"
down_revision = "02ea03a5ada0"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("rss_feeds", sa.Column("etag", sa.Text, nullable=True))


def downgrade():
    op.drop_column("rss_feeds", "etag")
