"""create championships table

Revision ID: 89d8976a8624
Revises: 940c1a7e24a7
Create Date: 2025-11-23 00:01:06.644287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.domain.championship.value_objects import ChampionshipStatusEnum


# revision identifiers, used by Alembic.
revision: str = '89d8976a8624'
down_revision: Union[str, Sequence[str], None] = '940c1a7e24a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'championships',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('organizer_id', sa.Integer(),
                  sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False,
                  server_default=ChampionshipStatusEnum.INSCRIPTIONS_OPEN.value),
        sa.Column('sets_to_win', sa.Integer(), nullable=False),
        sa.Column('points_per_set', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.DateTime(),
                  server_default=sa.text('now()')),
        sa.Column('end_date', sa.DateTime(),
                  server_default=sa.text('now()')),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('logo_url', sa.String(), nullable=True),
        sa.Column('max_teams', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=False),
                  nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=False), nullable=False,
                  server_default=sa.text('now()'),
                  onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('championships')
    pass
