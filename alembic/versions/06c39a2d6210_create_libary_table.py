"""create libary table

Revision ID: 06c39a2d6210
Revises: 3df42bf575fc
Create Date: 2023-10-07 19:16:25.458766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06c39a2d6210'
down_revision: Union[str, None] = '3df42bf575fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("libarys",
        sa.Column("book_id",sa.Integer(),primary_key=True,nullable=False),
        sa.Column("user_id",sa.Integer(),primary_key=True,nullable=False)
    )
    op.create_foreign_key(constraint_name="libary_book_fk",source_table="libarys",referent_table="books",
                          local_cols=["book_id"],remote_cols=["id"],ondelete="CASCADE")
    op.create_foreign_key(constraint_name="libary_user_fk",source_table="libarys",referent_table="users",
                          local_cols=["user_id"],remote_cols=["id"],ondelete="CASCADE")

def downgrade() -> None:
    op.drop_constraint("libary_user_fk","libarys")
    op.drop_constraint("libary_book_fk","libarys")
    op.drop_column("libarys","user_id")
    op.drop_column("libarys","book_id")
    op.drop_table("libarys")

