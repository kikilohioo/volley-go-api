class TeamDomainException(Exception):
    """Base class for all team-related domain exceptions."""
    pass


# --- DATOS BÁSICOS DEL EQUIPO ---
class InvalidTeamNameException(TeamDomainException):
    """Raised when the team name is invalid."""
    pass


class DuplicateTeamNameException(TeamDomainException):
    """Raised when a team with the same name already exists in a championship."""
    pass


# --- RELACIONES ---
class InvalidChampionshipException(TeamDomainException):
    """Raised when the associated championship is invalid or does not exist."""
    pass


class InvalidTeamOwnerException(TeamDomainException):
    """Raised when the team owner (user) is invalid or not allowed."""
    pass


# --- ESTADÍSTICAS / RESULTADOS ---
class InvalidTeamStatsException(TeamDomainException):
    """Raised when invalid statistics are provided for a team."""
    pass


class NegativeStatsException(InvalidTeamStatsException):
    """Raised when stats contain negative values."""
    pass


class StatsUpdateNotAllowedException(InvalidTeamStatsException):
    """Raised when stats are updated in an invalid state."""
    pass


# --- ESTADO DEL EQUIPO ---
class TeamInactiveException(TeamDomainException):
    """Raised when an action is attempted on an inactive team."""
    pass


# --- INSCRIPCIÓN / PARTICIPACIÓN ---
class TeamAlreadyRegisteredException(TeamDomainException):
    """Raised when the team is already registered in a championship."""
    pass


class TeamRegistrationClosedException(TeamDomainException):
    """Raised when trying to register a team after registration is closed."""
    pass


# --- NO ENCONTRADO ---
class TeamNotFoundException(TeamDomainException):
    """Raised when a team is not found."""
    pass
