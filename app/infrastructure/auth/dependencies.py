# app/infrastructure/auth/auth_dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.application.mappers import to_domain
from app.domain.user.entities import User
from app.infrastructure.database import get_session
from app.infrastructure.user.sqlalchemy_user_model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.auth.jwt_service import JWTService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='No se pudo validar las credenciales',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    payload = JWTService.verify_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get('user_id')
    if user_id is None:
        raise credentials_exception

    user = session.get(UserModel, user_id)
    if not user:
        raise credentials_exception

    user = to_domain(user, User)
    
    return user
