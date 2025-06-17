"""product images and videos

Revision ID: 3517baee24c2
Revises: 3d86ec6eb2fb
Create Date: 2025-06-17 12:40:46.071448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3517baee24c2'
down_revision: Union[str, None] = '3d86ec6eb2fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
