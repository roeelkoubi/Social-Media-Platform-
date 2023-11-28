"""add content column to posts table

Revision ID: 234690659cff
Revises: 1933a2ec27cb
Create Date: 2023-11-28 16:01:04.133258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '234690659cff'
down_revision: Union[str, None] = '1933a2ec27cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
