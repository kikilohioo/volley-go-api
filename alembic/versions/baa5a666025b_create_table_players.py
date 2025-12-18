"""create table players

Revision ID: baa5a666025b
Revises: 1bb74927bd82
Create Date: 2025-12-14 00:56:44.731891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'baa5a666025b'
down_revision: Union[str, Sequence[str], None] = '1bb74927bd82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'players',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(),
                  sa.ForeignKey('users.id'), nullable=False),
        sa.Column('team_id', sa.Integer(),
                  sa.ForeignKey('teams.id'), nullable=False),
        sa.Column('position', sa.String(), nullable=False),
        sa.Column('jersey_number', sa.Integer(), nullable=False, default=0),
        sa.Column('logo_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=False),
                  nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=False), nullable=False,
                  server_default=sa.text('now()'),
                  onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('players')
    pass
