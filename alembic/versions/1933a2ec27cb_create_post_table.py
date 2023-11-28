"""create post table

Revision ID: 1933a2ec27cb
Revises: 
Create Date: 2023-11-27 13:49:16.169566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1933a2ec27cb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True)
                    ,sa.Column("title",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
