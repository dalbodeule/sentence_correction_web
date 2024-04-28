"""dataset add status column

Revision ID: b2f4f42c9e64
Revises: 130d08ba39af
Create Date: 2024-04-25 12:21:30.534293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b2f4f42c9e64'
down_revision: Union[str, None] = '130d08ba39af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum('PENDING', 'APPROVED', 'REJECTED', name='datasetstatus').create(op.get_bind())
    op.add_column('dataset', sa.Column('status', postgresql.ENUM('PENDING', 'APPROVED', 'REJECTED', name='datasetstatus', create_type=False), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dataset', 'status')
    sa.Enum('PENDING', 'APPROVED', 'REJECTED', name='datasetstatus').drop(op.get_bind())
    # ### end Alembic commands ###