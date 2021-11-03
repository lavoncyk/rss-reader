"""Add icon column on rss_feeds

Revision ID: ccef88865712
Revises: 948ea6926116
Create Date: 2021-11-03 17:22:35.095782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ccef88865712"
down_revision = "948ea6926116"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("rss_feeds", sa.Column("icon", sa.Text, nullable=True))


def downgrade():
    op.drop_column("rss_feeds", "icon")
