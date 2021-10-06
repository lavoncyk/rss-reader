"""Create posts table

Revision ID: 13387d511936
Revises: f54ad347fde1
Create Date: 2021-09-21 10:43:08.617429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "13387d511936"
down_revision = "f54ad347fde1"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("rss_feed_id", sa.Integer, sa.ForeignKey("rss_feeds.id"),
                  nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("published_at", sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table("posts")
