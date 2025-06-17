"""product images and videos

Revision ID: a500fb99919a
Revises: 3517baee24c2
Create Date: 2025-06-17 12:42:49.489511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a500fb99919a'
down_revision: Union[str, None] = '3517baee24c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
