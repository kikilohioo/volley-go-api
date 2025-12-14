# app/api/auth/routes.py

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from app.api.auth.dependencies import get_current_user, get_file_service, get_login_form, get_repo
from app.api.auth.schemas import LoginResponse, RegisterUserDTO, RegisterUserRequest
from app.api.user.dependencies import get_password_service
from app.api.user.schemas import UserResponse
from app.application.auth.use_cases import LoginUserUseCase, RegisterUserUseCase
from app.application.mappers import to_schema
from app.infrastructure.auth.password_service import PasswordService


router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post('/login')
async def login(user_credentials=Depends(get_login_form), repo=Depends(get_repo)):
    use_case = LoginUserUseCase(repo, PasswordService)

    response = use_case.execute(
        user_credentials.username, user_credentials.password)

    return response


@router.get('/check', status_code=status.HTTP_204_NO_CONTENT)
async def check_session(current_user=Depends(get_current_user)):
    pass


@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(email: str = Form(...),
                        password: str = Form(...),
                        full_name: str = Form(...),
                        avatar: UploadFile | None = File(None),
                        repo=Depends(get_repo),
                        password_service=Depends(get_password_service),
                        file_service=Depends(get_file_service)):
    use_case = RegisterUserUseCase(repo, password_service, file_service)
    
    # TODO: revisar bien este dto para cambiar nombre y otras cosas
    dto = RegisterUserDTO(
        email=email,
        password=password,
        full_name=full_name,
        avatar=avatar
    )
    
    user = await use_case.execute(dto)

    return user
