"""owner book foreign key

Revision ID: 3df42bf575fc
Revises: 012f30dc6c93
Create Date: 2023-10-07 18:21:12.062779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3df42bf575fc'
down_revision: Union[str, None] = '012f30dc6c93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("books",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("book_user_fk",source_table="books",referent_table="users",
                          local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    


def downgrade() -> None:
    op.drop_constraint(constraint_name="book_user_fk",table_name="books")
    op.drop_column("books","owner_id")
    pass
