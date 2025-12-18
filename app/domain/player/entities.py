from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Player:
    id: int | None = None

    # Relaciones
    user_id: int | None = None
    team_id: int | None = None

    # Info del jugador dentro del equipo
    position: str | None = None        # middle_blocker, opposite_spiker, setter, etc
    jersey_number: int | None = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)