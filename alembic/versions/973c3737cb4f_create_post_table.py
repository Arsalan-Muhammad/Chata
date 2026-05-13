"""Create post table

Revision ID: 973c3737cb4f
Revises: 
Create Date: 2026-05-12 16:40:46.655805

"""
from email.policy import default
from time import timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '973c3737cb4f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id' , sa.Integer ,primary_key=True , nullable=False ),
                    sa.Column('title' , sa.String()  , nullable=False ),
                    sa.Column('content' , sa.String() ,nullable=False ),
                    sa.Column('published' , sa.Boolean() , nullable=False , default=True),
                    sa.Column('created_at' , sa.TIMESTAMP(timezone=True) , nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
