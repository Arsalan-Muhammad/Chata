"""add foreign_key to post table

Revision ID: 38355ec3c999
Revises: f670172631e5
Create Date: 2026-05-13 15:07:57.036986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38355ec3c999'
down_revision: Union[str, Sequence[str], None] = 'f670172631e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts' , sa.Column('owner_id' , sa.Integer() , nullable=False))
    op.create_foreign_key('post_users_fk' , source_table='posts' , referent_table='users' , local_cols=['owner_id'] , remote_cols=['id'] , ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('post_users_fk' , table_name='posts')
    op.drop_column('posts' , 'owner_id')
    pass
