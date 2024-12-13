"""profile model

Revision ID: 31594355e329
Revises: cf7c7e7b6e1d
Create Date: 2024-12-13 20:21:58.567702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '31594355e329'
down_revision: Union[str, None] = 'cf7c7e7b6e1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('karma', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('profile_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'profiles', ['profile_id'], ['id'])
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'profile_id')
    op.drop_table('profiles')
    # ### end Alembic commands ###
