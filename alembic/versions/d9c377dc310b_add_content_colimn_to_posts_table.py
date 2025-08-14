"""add content colimn to posts table

Revision ID: d9c377dc310b
Revises: b70e778b5f73
Create Date: 2025-08-04 22:38:43.781482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9c377dc310b'
down_revision: Union[str, Sequence[str], None] = 'b70e778b5f73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('Posts','content')
    pass
