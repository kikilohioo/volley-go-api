# app/domain/championship/exceptions.py


class ChampionshipDomainException(Exception):
    """Base class for all championship-related domain exceptions."""
    pass


# --- FECHAS Y CRONOGRAMA ---
class ChampionshipDateException(ChampionshipDomainException):
    """Raised when there is an issue with championship dates."""
    pass


class ChampionshipStartAfterEndException(ChampionshipDateException):
    """Raised when the start date is after the end date."""
    pass


class ChampionshipOverlapException(ChampionshipDateException):
    """Raised when the championship dates overlap with another championship of the same type."""
    pass


class ChampionshipPastDateException(ChampionshipDateException):
    """Raised when trying to schedule a championship in the past."""
    pass


# --- ESTADO DEL CAMPEONATO ---
class InvalidChampionshipStatusException(ChampionshipDomainException):
    """Raised when an invalid status is provided for a championship."""
    pass


class ChampionshipActionNotAllowedException(InvalidChampionshipStatusException):
    """Raised when an action is attempted on a championship not allowed by its current status."""
    pass


# --- TIPO DE CAMPEONATO ---
class InvalidChampionshipTypeException(ChampionshipDomainException):
    """Raised when an invalid championship type is provided."""
    pass


# --- PARTICIPANTES / EQUIPOS ---
class MinParticipantsException(ChampionshipDomainException):
    """Raised when there are not enough participants to start a championship."""
    pass


class MaxParticipantsException(ChampionshipDomainException):
    """Raised when adding a participant exceeds the maximum allowed."""
    pass


class DuplicateParticipantException(ChampionshipDomainException):
    """Raised when a participant or team is already registered in the championship."""
    pass


class InactiveParticipantException(ChampionshipDomainException):
    """Raised when trying to add a participant that is not active or eligible."""
    pass


# --- INSCRIPCIONES Y UBICACIÓN ---
class RegistrationClosedException(ChampionshipDomainException):
    """Raised when registration is attempted after the registration deadline."""
    pass


class InvalidVenueException(ChampionshipDomainException):
    """Raised when the championship venue is invalid or unavailable."""
    pass


# --- NO ENCONTRADO ---
class ChampionshipNotFoundException(ChampionshipDomainException):
    """Raised when a championship is not found."""
    pass
