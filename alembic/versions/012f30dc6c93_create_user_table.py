"""create user table

Revision ID: 012f30dc6c93
Revises: 326aefc28b08
Create Date: 2023-10-07 17:38:38.055149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '012f30dc6c93'
down_revision: Union[str, None] = '326aefc28b08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",sa.Column("id",sa.Integer(),primary_key=True,nullable=False),
                    sa.Column("name",sa.String(),nullable=False),
                    sa.Column("email",sa.String(),nullable=False),
                    sa.Column("password",sa.String(),nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")),
                    )


def downgrade() -> None:
    op.drop_table("users")
