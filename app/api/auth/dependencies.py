# app/api/auth/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.infrastructure.database import get_session
from app.infrastructure.file_service import UserFileService
from app.infrastructure.user.sqlalchemy_repository import SQLAlchemyUserRepository
from app.infrastructure.auth.jwt_service import JWTService
from app.application.user.use_cases import GetCurrentUserUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Credenciales invalidas porfavor verifique',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    # decode token
    try:
        token_data = JWTService.verify_access_token(token)
    except:
        raise credentials_exception

    if not token_data['user_id']:
        raise credentials_exception

    # load user via use case
    user_repo = SQLAlchemyUserRepository(db)
    use_case = GetCurrentUserUseCase(user_repo)

    try:
        return use_case.execute(int(token_data['user_id']))
    except:
        raise credentials_exception


async def get_repo(session=Depends(get_session)):
    return SQLAlchemyUserRepository(session)

async def get_login_form(form_data: OAuth2PasswordRequestForm = Depends()):
    return form_data

def get_file_service():
    return UserFileService()