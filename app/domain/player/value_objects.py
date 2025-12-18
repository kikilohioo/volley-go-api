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
            raise InvalidPlayerPositionException("Player position must be either 'setter', 'outside_hitter', 'middle_blocker', 'opposite_spiker', 'libero'")


@dataclass(frozen=True)
class JerseyNumber:
    value: int

    def __post_init__(self):
        if self.value <= 0 or self.value > 99:
            raise InvalidJerseyNumberException(
                "Jersey number must be between 1 and 99"
            )
