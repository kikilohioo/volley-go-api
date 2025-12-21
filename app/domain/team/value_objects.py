from dataclasses import dataclass
from enum import Enum

from .exceptions import (
    InvalidTeamNameException,
    InvalidTeamStatsException,
)

class TeamName:
    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) < 3:
            raise InvalidTeamNameException(
                "El nombre del equipo debe tener al menos 3 caracteres"
            )
            
class TeamStats:
    wins: int = 0
    losses: int = 0
    points: int = 0
    sets_won: int = 0
    sets_lost: int = 0

    def __post_init__(self):
        for field_name, value in vars(self).items():
            if value < 0:
                raise InvalidTeamStatsException(
                    f"{field_name} no puede ser negativo"
                )