"""Create categories table & Add FK rss_feeds -> categories.

Revision ID: d8fa81723cf3
Revises: f2ef3bbe6225
Create Date: 2021-11-02 15:22:02.671695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d8fa81723cf3"
down_revision = "f2ef3bbe6225"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )

    op.add_column(
        "rss_feeds",
        sa.Column("category_id", sa.Integer, sa.ForeignKey("categories.id"),
                  nullable=True))


def downgrade():
    op.drop_column("rss_feeds", "category_id")
    op.drop_table("categories")
