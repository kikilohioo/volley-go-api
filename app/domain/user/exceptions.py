# app/domain/user/exceptions.py


class UserDomainException(Exception):
    '''Base class for all user-related domain exceptions.'''
    pass


class UserAlreadyExistsException(UserDomainException):
    '''Raised when trying to create a user with an email that already exists.'''
    pass


class UserNotFoundException(UserDomainException):
    '''Raised when a user is not found in the repository.'''
    pass


class InvalidCredentialsException(UserDomainException):
    '''Raised when login credentials are incorrect.'''
    pass


class InactiveUserException(UserDomainException):
    '''Raised when the user account is disabled.'''
    pass


class InvalidUserRoleException(UserDomainException):
    '''Raised when the user role is invalid.'''
    pass
