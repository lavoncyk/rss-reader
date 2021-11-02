"""Add created_at to posts

Revision ID: f2ef3bbe6225
Revises: c88375693a39
Create Date: 2021-11-02 15:19:17.813861

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f2ef3bbe6225"
down_revision = "c88375693a39"
branch_labels = None
depends_on = None


t_name = "posts"
t_posts = sa.Table(
    t_name,
    sa.MetaData(bind=None),
    sa.Column("created_at", sa.DateTime, nullable=True),
)


def upgrade():
    op.add_column(t_name, sa.Column("created_at", sa.DateTime, nullable=True))
    op.execute(t_posts.update().values(created_at=datetime.now()))
    op.alter_column(t_name, "created_at", nullable=False)


def downgrade():
    op.drop_column(t_name, "created_at")
