"""init

Revision ID: 63700068619b
Revises: 
Create Date: 2024-05-31 15:18:45.851125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63700068619b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stacks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('surname', sa.String(length=200), nullable=False),
    sa.Column('username', sa.String(length=200), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('role', sa.Enum('admin', 'recruiter', 'hiring_manager', 'resource_manager', name='roles'), nullable=False),
    sa.Column('password_hash', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('stacks')
    # ### end Alembic commands ###