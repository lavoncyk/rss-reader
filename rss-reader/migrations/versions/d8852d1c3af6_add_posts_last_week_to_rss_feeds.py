"""Add posts_last_week to rss_feeds

Revision ID: d8852d1c3af6
Revises: ccef88865712
Create Date: 2021-11-05 10:46:32.316182

"""

from datetime import datetime
from datetime import timedelta

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d8852d1c3af6"
down_revision = "ccef88865712"
branch_labels = None
depends_on = None


t_name = "rss_feeds"
t_rss_feeds = sa.Table(
    t_name,
    sa.MetaData(bind=None),
    sa.Column("posts_last_week", sa.DateTime, nullable=True),
)


def set_posts_last_week(connection):
    last_week_start = datetime.utcnow() - timedelta(days=7)
    sql = sa.text("""
        UPDATE rss_feeds AS r
           SET posts_last_week =
               (SELECT COUNT(*)
                  FROM posts AS p
                 WHERE p.published_at >= :last_week_start
                   AND p.rss_feed_id = r.id); 
    """)
    connection.execute(
        sql,
        last_week_start=last_week_start,
    )


def upgrade():
    op.add_column(
        t_name, sa.Column("posts_last_week", sa.Integer, nullable=True,
                          default=0))

    connection = op.get_bind()
    set_posts_last_week(connection)
    op.alter_column(t_name, "posts_last_week", nullable=False)


def downgrade():
    op.drop_column(t_name, "posts_last_week")
