# app/api/user/routes.py

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from app.api.auth.dependencies import get_file_service
from app.api.auth.routes import get_repo
from app.api.user.dependencies import get_password_service
from app.api.user.schemas import SetUserRoleRequest, UpdateUserDTO, UpdateUserRequest, UserResponse
from app.application.mappers import to_schema
from app.application.user.use_cases import DeleteUserUseCase, GetCurrentUserUseCase, GetUserByIdUseCase, UpdateCurrentUserUseCase
from app.infrastructure.auth.dependencies import get_current_user


router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/me', response_model=UserResponse)
async def get_my_user(current_user=Depends(get_current_user), repo=Depends(get_repo)):
    use_case = GetCurrentUserUseCase(repo)
    current_user = use_case.execute(current_user.id)
    return current_user


@router.put('/me', response_model=UserResponse)
async def update_user(email: str | None = Form(None),
                      new_password: str | None = Form(None),
                      full_name: str | None = Form(None),
                      avatar: UploadFile | None = File(None),
                      repo=Depends(get_repo),
                      password_service=Depends(get_password_service),
                      current_user=Depends(get_current_user),
                      file_service=Depends(get_file_service)):
    use_case = UpdateCurrentUserUseCase(repo, password_service, file_service)
    
    # TODO: revisar bien este dto para cambiar nombre y otras cosas
    dto = UpdateUserDTO(
        email=email,
        full_name=full_name
    )
    
    if new_password is not None: dto.password = new_password
    if avatar is not None: dto.avatar = avatar
    
    updated_current_user = await use_case.execute(
        current_user=current_user, updated_user=dto)

    return updated_current_user


@router.put('/me/set-role', response_model=UserResponse)
async def update_user(
    user_role: SetUserRoleRequest,
    repo=Depends(get_repo),
    password_service=Depends(get_password_service),
    current_user=Depends(get_current_user),
    file_service=Depends(get_file_service)
):
    use_case = UpdateCurrentUserUseCase(repo, password_service, file_service)
    
    dto = UpdateUserDTO(
        role=user_role.role
    )
    
    updated_current_user = await use_case.execute(
        current_user=current_user, 
        updated_user=dto
    )

    return updated_current_user


@router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: int, repo=Depends(get_repo), current_user=Depends(get_current_user)):
    use_case = GetUserByIdUseCase(repo)
    user = use_case.execute(user_id)

    return user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, repo=Depends(get_repo), current_user=Depends(get_current_user)):
    use_case = DeleteUserUseCase(repo)
    user = use_case.execute(user_id)
    return user
