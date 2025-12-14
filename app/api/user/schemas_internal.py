# app/domain/user/schemas_internal.py

from app.api.user.schemas import UserResponse


class UserInternal(UserResponse):
    """
    Esquema interno, NO expuesto en la API.
    Incluye la contraseña para tests y lógica interna.
    """
    password: str
