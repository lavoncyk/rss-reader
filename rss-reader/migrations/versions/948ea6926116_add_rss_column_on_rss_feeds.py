"""Add rss column on rss_feeds

Revision ID: 948ea6926116
Revises: 5ba9cd4297ea
Create Date: 2021-11-03 17:10:24.046760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "948ea6926116"
down_revision = "5ba9cd4297ea"
branch_labels = None
depends_on = None


t_name = "rss_feeds"
t_rss_feeds = sa.Table(
    t_name,
    sa.MetaData(bind=None),
    sa.Column("url", sa.Text, nullable=False),
    sa.Column("rss", sa.Text, nullable=True),
)


def upgrade():
    op.add_column(t_name, sa.Column("rss", sa.Text, nullable=True))
    op.execute(t_rss_feeds.update().values(rss=t_rss_feeds.c.url))
    op.alter_column(t_name, "rss", nullable=False)


def downgrade():
    op.drop_column(t_name, "rss")
