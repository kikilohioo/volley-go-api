# app/application/auth/use_cases.py

from datetime import datetime
from app.api.auth.schemas import RegisterUserDTO, RegisterUserRequest
from app.api.user.schemas import UserResponse
from app.application.mappers import to_schema
from app.domain.user.entities import User
from app.domain.user.exceptions import InvalidCredentialsException, UserAlreadyExistsException
from app.domain.user.repositories import IUserRepository
from app.infrastructure.auth.jwt_service import JWTService
from app.infrastructure.auth.password_service import PasswordService
from app.infrastructure.file_service import UserFileService
from app.infrastructure.mappers import to_domain


class LoginUserUseCase:
    def __init__(self, repo: IUserRepository, password_service: PasswordService):
        self.repo = repo
        self.password_service = password_service

    def execute(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user:
            raise InvalidCredentialsException('Invalid credentials')

        if not self.password_service.verify(password, user.password.value):
            raise InvalidCredentialsException('Invalid credentials')

        token = JWTService.create_access_token({'user_id': user.id})
        return {'access_token': token, 'user': to_schema(user, UserResponse)}


class RegisterUserUseCase:
    def __init__(self, user_repo: IUserRepository, password_service: PasswordService, file_service: UserFileService):
        self.user_repo = user_repo
        self.password_service = password_service
        self.file_service = file_service

    async def execute(self, new_user: RegisterUserDTO) -> User:
        exist_user = self.user_repo.get_by_email(new_user.email)
        if exist_user is not None:
            raise UserAlreadyExistsException("User with that email already exists")

        hashed_password = self.password_service.hash(new_user.password)

        user = User(
            email=new_user.email,
            password=hashed_password,
            full_name=new_user.full_name,
            avatar_url=None
        )

        # Procesar avatar si viene
        if new_user.avatar:
            temp_path = await self.file_service.save_temp_avatar(new_user.avatar)
            filename = await self.file_service.commit_avatar(temp_path)
            user.avatar_url = f"/media/avatars/{filename}"

        created_user = self.user_repo.create(user)
        return to_schema(created_user, UserResponse)

# TODO: Implement ForgotPasswordUseCase and ResetPasswordUseCase in the future.