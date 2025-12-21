# app/application/user/use_cases.py

from app.api.user.schemas import UpdateUserDTO, UpdateUserRequest, UserResponse
from app.application.mappers import to_domain, to_schema
from app.domain.user.entities import User
from app.domain.user.exceptions import UserAlreadyExistsException, UserNotFoundException
from app.domain.user.repositories import IUserRepository
from dataclasses import replace

from app.infrastructure.auth.password_service import PasswordService
from app.infrastructure.file_service import UserFileService


class GetCurrentUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException('Usuario no encontrado')
        return to_schema(user, UserResponse)


class UpdateCurrentUserUseCase:
    def __init__(self, user_repo: IUserRepository, password_service: PasswordService, file_service: UserFileService):
        self.user_repo = user_repo
        self.password_service = password_service
        self.file_service = file_service

    async def execute(self, updated_user: UpdateUserDTO, current_user: User):
        # 1. Crear copia del usuario actual
        working_copy = replace(current_user)

        # 2. Validación: email único si lo cambia (solo si updated_user.email NO es None)
        if updated_user.email and updated_user.email != current_user.email.value:
            exist_user = self.user_repo.get_by_email(updated_user.email)
            if exist_user:
                raise UserAlreadyExistsException("Ya existe un usuario con este email")
            working_copy.email = updated_user.email

        # 3. Procesar contraseña si viene
        if updated_user.password:
            hashed_password = self.password_service.hash(updated_user.password)
            working_copy.password = hashed_password

        # 4. Procesar avatar si viene
        if updated_user.avatar:
            temp = await self.file_service.save_temp_avatar(updated_user.avatar)
            final_name = await self.file_service.commit_avatar(temp)
            working_copy.avatar_url = f"/media/avatars/{final_name}"

        # 5. Aplicar merge para otros campos (full_name, role, etc)
        # Asumiendo que to_domain convierte el DTO a diccionario o objeto de dominio
        updates = to_domain(updated_user, User, partial=True)
        
        # Si 'updates' es un diccionario:
        iterable_updates = updates.items() if isinstance(updates, dict) else updates.__dict__.items()

        for field, value in iterable_updates:
            # Importante: Si el valor es None, lo ignoramos para mantener el valor original del usuario
            if value is None:
                continue

            # Campos especiales ya manejados arriba
            if field in ("email", "password", "avatar"):
                continue
            
            # Actualizamos el working_copy solo si hay un valor nuevo
            setattr(working_copy, field, value)

        # 6. Persistir cambios
        updated = self.user_repo.update(working_copy)
        if not updated:
            raise UserNotFoundException("Usuario no encontrado")

        return to_schema(updated, UserResponse)


class GetUserByIdUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundException('Usuario no encontrado')

        return to_schema(user, UserResponse)


class DeleteUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException('Usuario no encontrado')

        result = self.user_repo.delete(user_id)
        if not result:
            return True

        return False
