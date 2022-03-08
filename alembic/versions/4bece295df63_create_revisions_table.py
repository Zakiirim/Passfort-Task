"""Create revisions table

Revision ID: 4bece295df63
Revises: 6500b01d0485
Create Date: 2022-03-08 16:15:08.281827

"""
import uuid

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = '4bece295df63'
down_revision = '6500b01d0485'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "revisions",
        sa.Column(
            "revision",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
        ),
        sa.Column(
            "timestamp",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "content",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "title_id",
            sa.Integer(),
            sa.ForeignKey("titles.id"),
            nullable=False,
        )
    )


def downgrade():
    op.drop_table("revisions")
