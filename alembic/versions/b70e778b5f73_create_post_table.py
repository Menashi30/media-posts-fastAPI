"""create post table

Revision ID: b70e778b5f73
Revises: 
Create Date: 2025-08-03 00:38:57.109412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b70e778b5f73'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("Posts",sa.Column('id',sa.Integer(),nullable = False, primary_key = True),
                    sa.Column('title',sa.String(),nullable = False))
    pass


def downgrade() -> None:
    op.downgrade("Posts")
    pass
