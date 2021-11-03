"""Add on-delete to FKs.

Revision ID: 5ba9cd4297ea
Revises: d8fa81723cf3
Create Date: 2021-11-03 14:28:43.001481

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "5ba9cd4297ea"
down_revision = "d8fa81723cf3"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("posts_rss_feed_id_fkey", "posts", type_="foreignkey")
    op.create_foreign_key(
        "posts_rss_feed_id_fkey",
        "posts",
        "rss_feeds",
        ["rss_feed_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint("rss_feeds_category_id_fkey", "rss_feeds",
                       type_='foreignkey')
    op.create_foreign_key(
        "rss_feeds_category_id_fkey",
        "rss_feeds",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade():
    op.drop_constraint("rss_feeds_category_id_fkey", "rss_feeds",
                       type_="foreignkey")
    op.create_foreign_key(
        "rss_feeds_category_id_fkey",
        "rss_feeds",
        "categories",
        ["category_id"],
        ["id"],
    )

    op.drop_constraint("posts_rss_feed_id_fkey", "posts", type_="foreignkey")
    op.create_foreign_key(
        "posts_rss_feed_id_fkey"
        "posts",
        "rss_feeds",
        ["rss_feed_id"],
        ["id"],
    )
