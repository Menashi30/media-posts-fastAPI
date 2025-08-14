"""add remaining columns to the Posts table

Revision ID: 082713af6c2f
Revises: e88d9de8426d
Create Date: 2025-08-05 15:44:01.806918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '082713af6c2f'
down_revision: Union[str, Sequence[str], None] = 'e88d9de8426d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts',sa.Column('published',sa.Boolean(), server_default='TRUE',nullable=False))
    op.add_column('Posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('Posts','published')
    op.drop_column('Posts','created_at')
    pass
