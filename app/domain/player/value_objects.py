from dataclasses import dataclass
from enum import Enum

from .exceptions import (
    InvalidJerseyNumberException,
    InvalidPlayerPositionException,
    InvalidTeamNameException,
    InvalidTeamStatsException,
)


class PlayerPositionEnum(str, Enum):
    SETTER = "setter"
    OUTSIDE_HITTER = "outside_hitter"
    MIDDLE_BLOCKER = "middle_blocker"
    OPPOSITE_SPIKER = "opposite_spiker"
    LIBERO = "libero"
    
    
@dataclass(frozen=True)
class PlayerPosition:
    value: str

    def __post_init__(self):
        if self.value not in PlayerPositionEnum._value2member_map_:
            raise InvalidPlayerPositionException("Posicion de jugador incorrecta")


@dataclass(frozen=True)
class JerseyNumber:
    value: int

    def __post_init__(self):
        if self.value <= 0 or self.value > 99:
            raise InvalidJerseyNumberException(
                "El numero de la camiseta tiene que ser entre 1 y 99"
            )
