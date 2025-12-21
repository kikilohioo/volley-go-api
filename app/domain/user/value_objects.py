# app/domain/user/value_objects.py

import re
from enum import Enum
from dataclasses import dataclass
from app.domain.user.exceptions import InvalidCredentialsException, InvalidUserRoleException


@dataclass(frozen=True)
class UserEmail:
    value: str

    def __post_init__(self):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', self.value):
            raise InvalidCredentialsException('Formato de correo electronico invalido')


@dataclass(frozen=True)
class UserPassword:
    value: str

    def __post_init__(self):
        if len(self.value) < 8:
            raise InvalidCredentialsException(
                'La contraseña debe tener al menos 8 caracteres de largo')


class UserRoleTypeEnum(str, Enum):
    PLAYER = 'player'
    ORGANIZER = 'organizer'


@dataclass(frozen=True)
class UserRole:
    value: str

    def __post_init__(self):
        if self.value not in UserRoleTypeEnum._value2member_map_:
            raise InvalidUserRoleException(
                "El rol solo puede ser Jugador u Organizador")

    def __str__(self):
        return self.value
