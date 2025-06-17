"""product images and videos

Revision ID: 96618fa85276
Revises: 2aa9096054ef
Create Date: 2025-06-17 12:38:08.406935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96618fa85276'
down_revision: Union[str, None] = '2aa9096054ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
