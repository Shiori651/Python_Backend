"""Create books table

Revision ID: 326aefc28b08
Revises: 
Create Date: 2023-10-07 17:22:21.010243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '326aefc28b08'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("books",sa.Column("id", sa.Integer(),primary_key=True, nullable=False),
                    sa.Column("name",sa.String(),nullable=False),
                    sa.Column("isbn",sa.String(),nullable=False),
                    sa.Column("explanation",sa.String(),nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()"))
                    )
    pass


def downgrade() -> None:
    op.drop_table("books")
