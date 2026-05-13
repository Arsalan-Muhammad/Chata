"""create users table

Revision ID: f670172631e5
Revises: 973c3737cb4f
Create Date: 2026-05-13 15:06:08.828872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f670172631e5'
down_revision: Union[str, Sequence[str], None] = '973c3737cb4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
 op.create_table('users',
                     sa.Column('id' , sa.Integer() , nullable=False , primary_key=True),
                     sa.Column('email' , sa.String() , nullable=False , unique=True),
                     sa.Column('password' , sa.Integer() , nullable=False),
                     sa.Column('created_at' , sa.TIMESTAMP(timezone=True) , server_default=sa.text('now()') , nullable=False)
                     ) 


def downgrade() -> None:
 op.drop_table("users")
