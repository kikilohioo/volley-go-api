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
                "El nombre del campeonato tiene que tener al menos 3 caracteres")


@dataclass(frozen=True)
class ChampionshipDates:
    start_date: datetime
    end_date: datetime

    def __post_init__(self):
        if self.end_date <= self.start_date:
            raise ValueError("Fecha y hora de finalizacion debe ser posterior a fecha y hora de inicio")


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
            raise InvalidChampionshipStatusException("Tipo de campeonato incorrecto")


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
            raise InvalidChampionshipStatusException("Estado de campeonato incorrecto")
