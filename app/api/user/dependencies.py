# app/api/user/dependencies.py

from fastapi import Depends
from app.infrastructure.auth.password_service import PasswordService
from app.infrastructure.database import get_session
from app.infrastructure.user.sqlalchemy_repository import SQLAlchemyUserRepository


def get_password_service():
    return PasswordService()


async def get_repo(session=Depends(get_session)):
    return SQLAlchemyUserRepository(session)
