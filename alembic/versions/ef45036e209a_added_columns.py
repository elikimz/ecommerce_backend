"""added columns

Revision ID: ef45036e209a
Revises: d8286d9cbeb7
Create Date: 2025-06-23 12:53:40.072830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef45036e209a'
down_revision: Union[str, None] = 'd8286d9cbeb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('colors', sa.String(), nullable=True))
    op.add_column('products', sa.Column('warranty', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'warranty')
    op.drop_column('products', 'colors')
    # ### end Alembic commands ###
