"""product images and videos

Revision ID: 3d86ec6eb2fb
Revises: 436a379ea8cc
Create Date: 2025-06-17 12:40:23.380860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d86ec6eb2fb'
down_revision: Union[str, None] = '436a379ea8cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
