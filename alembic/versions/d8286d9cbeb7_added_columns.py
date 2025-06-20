"""added columns

Revision ID: d8286d9cbeb7
Revises: fc4dd8093d77
Create Date: 2025-06-20 10:50:34.118423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8286d9cbeb7'
down_revision: Union[str, None] = 'fc4dd8093d77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('customer_name', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('customer_email', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('customer_phone', sa.String(), nullable=False))
    op.alter_column('orders', 'total_amount',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('orders', 'shipping_address',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'shipping_address',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('orders', 'total_amount',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.drop_column('orders', 'customer_phone')
    op.drop_column('orders', 'customer_email')
    op.drop_column('orders', 'customer_name')
    # ### end Alembic commands ###
