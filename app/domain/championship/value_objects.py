# app/domain/championship/value_objects.py

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.domain.championship.exceptions import InvalidChampionshipStatusException


@dataclass(frozen=True)
class ChampionshipName:
    value: str

    def __post_init__(self):
        if not self.value or len(self.value) < 3:
            raise ValueError(
                "Championship name must be at least 3 characters long")


@dataclass(frozen=True)
class ChampionshipDates:
    start_date: datetime
    end_date: datetime

    def __post_init__(self):
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")


class ChampionshipTypeEnum(str, Enum):
    ROUND_ROBIN = 'round_robin'  # Todos contra todos, luego semis de los 4 mejores
    GROUPS_THEN_SEMIS = 'groups_then_semis' # Clasificación por grupos, luego semis
    GROUPS_THEN_QUARTERS = 'groups_then_quarters' # Clasificación por grupos, luego cuartos, semis, final
    KNOCKOUT = 'knockout'  # Eliminación directa, como 4tos, semis, final


@dataclass(frozen=True)
class ChampionshipType:
    value: str

    def __post_init__(self):
        if self.value not in ChampionshipTypeEnum._value2member_map_:
            raise InvalidChampionshipStatusException("Type must be either 'round_robin', 'groups_then_semis', 'groups_then_quarters' or 'knockout'")


class ChampionshipStatusEnum(str, Enum):
    UPCOMING = 'upcoming'
    INSCRIPTIONS_OPEN = 'inscriptions_open'
    INSCRIPTIONS_CLOSED = 'inscriptions_closed'
    ONGOING = 'ongoing'
    COMPLETED = 'completed'


@dataclass(frozen=True)
class ChampionshipStatus:
    value: str

    def __post_init__(self):
        if self.value not in ChampionshipStatusEnum._value2member_map_:
            raise InvalidChampionshipStatusException("Status must be either 'inscriptions_open', 'inscriptions_closed', 'ongoing' or 'completed'")
