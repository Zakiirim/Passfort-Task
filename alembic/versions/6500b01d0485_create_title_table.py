"""Create titles table

Revision ID: 6500b01d0485
Revises: 
Create Date: 2022-03-08 16:11:18.053661

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '6500b01d0485'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "titles",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            autoincrement=True,
        ),
        sa.Column(
            "title",
            sa.String(length=50),
            nullable=False,
            unique=True,
        )
    )


def downgrade():
    op.drop_table("titles")
