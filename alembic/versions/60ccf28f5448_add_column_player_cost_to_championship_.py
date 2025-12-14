"""add column player_cost to championship table

Revision ID: 60ccf28f5448
Revises: 89d8976a8624
Create Date: 2025-12-07 23:48:19.441397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60ccf28f5448'
down_revision: Union[str, Sequence[str], None] = '89d8976a8624'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "championships",
        sa.Column(
            "player_cost",
            sa.Float(precision=2),
            nullable=False,
            server_default="0"
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("championships", "player_cost")
