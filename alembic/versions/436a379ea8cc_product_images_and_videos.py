"""product images and videos

Revision ID: 436a379ea8cc
Revises: 96618fa85276
Create Date: 2025-06-17 12:38:52.651149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '436a379ea8cc'
down_revision: Union[str, None] = '96618fa85276'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
