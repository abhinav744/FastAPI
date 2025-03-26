"""Create address_id to users

Revision ID: ee6dc679f557
Revises: 6b1ba8a404ed
Create Date: 2025-03-26 09:51:50.243471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee6dc679f557'
down_revision: Union[str, None] = '6b1ba8a404ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_fk', source_table="users", referent_table="address",
                          local_cols=['address_id'], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('address_users_fk', table_name="users")
    op.drop_column('users', 'address_id')
