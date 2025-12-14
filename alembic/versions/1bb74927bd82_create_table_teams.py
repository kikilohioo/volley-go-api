"""create table teams

Revision ID: 1bb74927bd82
Revises: 60ccf28f5448
Create Date: 2025-12-14 00:44:44.806443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bb74927bd82'
down_revision: Union[str, Sequence[str], None] = '60ccf28f5448'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
