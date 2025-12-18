# app/api/player/dependencies.py

from fastapi import Depends
from app.infrastructure.player.sqlalchemy_repository import SQLAlchemyPlayerRepository
from app.infrastructure.database import get_session


async def get_repo(session=Depends(get_session)):
    return SQLAlchemyPlayerRepository(session)
