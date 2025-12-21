# app/domain/championship/entities.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from app.domain.user.entities import User
from .value_objects import ChampionshipDates, ChampionshipName, ChampionshipStatus, ChampionshipStatusEnum, ChampionshipType
from .exceptions import DuplicateParticipantException, MaxParticipantsException


@dataclass
class Championship:
    name: ChampionshipName
    type: ChampionshipType
    sets_to_win: int
    points_per_set: int
    location: str
    max_teams: int
    start_date: datetime
    end_date: datetime
    player_cost: float
    description: str | None = None
    logo_url: str | None = None
    organizer_id: int | None = None
    organizer: User | None = None
    id: int | None = None
    status: ChampionshipStatus = field(
        default_factory=lambda: ChampionshipStatus("upcoming")
    )
    teams: List[int] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # ---- DOMAIN METHOD: Inscribir equipo ----
    def add_team(self, team_id: int):
        if team_id in self.teams:
            raise DuplicateParticipantException(
                f"Equipo {team_id} ya esta registrado")
        if len(self.teams) >= self.max_teams:
            raise MaxParticipantsException(
                f"Maximo de equipos ({self.max_teams}) alcanzado")
        self.teams.append(team_id)
        self.updated_at = datetime.now()
