from dataclasses import dataclass, field
from datetime import datetime

from app.domain.team.value_objects import TeamName
from app.domain.user.entities import User
from .exceptions import InvalidTeamStatsException


@dataclass
class Team:
    name: TeamName
    championship_id: int
    user_id: int
    join_code: str

    # --- Stats ---
    wins: int = 0
    losses: int = 0
    points: int = 0
    sets_won: int = 0
    sets_lost: int = 0

    # --- Optional ---
    logo_url: str | None = None
    user: User | None = None

    # --- Metadata ---
    id: int | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def register_win(self, sets_won: int, sets_lost: int, points_earned: int):
        self._validate_sets(sets_won, sets_lost)

        self.wins += 1
        self.sets_won += sets_won
        self.sets_lost += sets_lost
        self.points += points_earned
        self.updated_at = datetime.now()

    def register_loss(self, sets_won: int, sets_lost: int):
        self._validate_sets(sets_won, sets_lost)

        self.losses += 1
        self.sets_won += sets_won
        self.sets_lost += sets_lost
        self.updated_at = datetime.now()

    def reset_stats(self):
        self.wins = 0
        self.losses = 0
        self.points = 0
        self.sets_won = 0
        self.sets_lost = 0
        self.updated_at = datetime.now()

    # ---------- VALIDATIONS ----------

    def _validate_sets(self, won: int, lost: int):
        if won < 0 or lost < 0:
            raise InvalidTeamStatsException(
                "Sets won/lost cannot be negative"
            )