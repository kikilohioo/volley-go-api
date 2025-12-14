# app/api/championship/dependencies.py

from fastapi import Depends
from app.infrastructure.championship.sqlalchemy_repository import SQLAlchemyChampionshipRepository
from app.infrastructure.database import get_session


async def get_repo(session=Depends(get_session)):
    return SQLAlchemyChampionshipRepository(session)
