"""add column join code to team

Revision ID: 88818549e615
Revises: baa5a666025b
Create Date: 2025-12-16 22:27:21.909631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88818549e615'
down_revision: Union[str, Sequence[str], None] = 'baa5a666025b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "teams",
        sa.Column("join_code", sa.String(length=12), nullable=True),
    )

    op.create_index(
        "ix_teams_join_code",
        "teams",
        ["join_code"],
        unique=True,
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_teams_join_code", table_name="teams")
    op.drop_column("teams", "join_code")
    pass
