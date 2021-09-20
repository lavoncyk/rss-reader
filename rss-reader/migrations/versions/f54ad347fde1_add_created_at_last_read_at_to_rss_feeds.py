"""Add created_at & last_read_at to rss_feeds

Revision ID: f54ad347fde1
Revises: e72c674d904a
Create Date: 2021-09-20 15:21:08.914254

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f54ad347fde1"
down_revision = "e72c674d904a"
branch_labels = None
depends_on = None


t_name = "rss_feeds"
t_rss_feeds = sa.Table(
    t_name,
    sa.MetaData(bind=None),
    sa.Column("last_read_at", sa.DateTime, nullable=True),
    sa.Column("created_at", sa.DateTime, nullable=True),
)


def upgrade():
    op.add_column(t_name, sa.Column("last_read_at", sa.DateTime, nullable=True))
    op.add_column(t_name, sa.Column("created_at", sa.DateTime, nullable=True))
    op.execute(t_rss_feeds.update().values(created_at=datetime.now()))
    op.alter_column(t_name, "created_at", nullable=False)


def downgrade():
    op.drop_column(t_name, "last_read_at")
    op.drop_column(t_name, "created_at")
