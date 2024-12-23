"""update post

Revision ID: 4c28e5da331b
Revises: dcca78e0d6a3
Create Date: 2024-12-23 19:12:08.084667

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '4c28e5da331b'
down_revision: Union[str, None] = 'dcca78e0d6a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('community_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'posts', 'communities', ['community_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey') # posts_community_id_fkey
    op.drop_column('posts', 'community_id')
    # ### end Alembic commands ###
