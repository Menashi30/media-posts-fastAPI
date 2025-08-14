"""add foreig key to the Posts table

Revision ID: e88d9de8426d
Revises: 7f5ea2e105ed
Create Date: 2025-08-05 12:55:21.858233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e88d9de8426d'
down_revision: Union[str, Sequence[str], None] = '7f5ea2e105ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts',sa.Column('owner_id',sa.Integer(),nullable = False))
    op.create_foreign_key('posts_users_fk',source_table = "Posts", referent_table = "Users",
                       local_cols = ['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name='Posts')
    op.drop_column('Posts','owner_id')
    pass
