class PlayerDomainException(Exception):
    """Base exception for Player domain"""
    pass


class PlayerNotFoundException(PlayerDomainException):
    pass


class PlayerAlreadyExistsException(PlayerDomainException):
    pass


class PlayerCreateException(PlayerDomainException):
    pass


class PlayerUpdateException(PlayerDomainException):
    pass


class PlayerDeleteException(PlayerDomainException):
    pass

class InvalidPlayerPositionException(PlayerDomainException):
    pass


class InvalidJerseyNumberException(PlayerDomainException):
    pass