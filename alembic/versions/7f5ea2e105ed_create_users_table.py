"""create users table

Revision ID: 7f5ea2e105ed
Revises: d9c377dc310b
Create Date: 2025-08-04 22:54:49.264007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f5ea2e105ed'
down_revision: Union[str, Sequence[str], None] = 'd9c377dc310b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("Users",sa.Column('id',sa.Integer(),nullable=False),
                            sa.Column('email',sa.String(),nullable=False),
                            sa.Column('password',sa.String(),nullable = False),
                            sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                                      server_default=sa.text('now()'),nullable=False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table("Users")
    pass
