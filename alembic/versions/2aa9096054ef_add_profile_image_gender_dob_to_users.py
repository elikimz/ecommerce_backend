"""Add profile_image, gender, dob to users

Revision ID: 2aa9096054ef
Revises: 94796631aaea
Create Date: 2025-06-13 12:21:21.424826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2aa9096054ef'
down_revision: Union[str, None] = '94796631aaea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('mpesa_receipt_number', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('transaction_date', sa.DateTime(), nullable=True))
    op.add_column('payments', sa.Column('merchant_request_id', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('checkout_request_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payments', 'checkout_request_id')
    op.drop_column('payments', 'merchant_request_id')
    op.drop_column('payments', 'transaction_date')
    op.drop_column('payments', 'mpesa_receipt_number')
    op.drop_column('payments', 'phone_number')
    # ### end Alembic commands ###
