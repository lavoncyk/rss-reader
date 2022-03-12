"""Create users table

Revision ID: cca62cbe5aad
Revises: d8852d1c3af6
Create Date: 2022-03-12 07:01:23.405305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cca62cbe5aad'
down_revision = 'd8852d1c3af6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        index_name=op.f("ix_users_email"),
        table_name="users",
        columns=["email"],
        unique=True,
    )


def downgrade():
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
