# app/domain/championship/repositories.py

from abc import ABC, abstractmethod
from typing import List, Tuple

from app.domain.team.entities import Team
from .entities import Championship


class IChampionshipRepository(ABC):
    @abstractmethod
    async def get_by_id(self, championship_id: int) -> Championship | None:
        pass

    @abstractmethod
    async def list(
        self,
        status: str | None = None,
        type: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Championship]:
        """Retorna varios campeonatos filtrando por status o tipo, con paginación"""
        pass

    @abstractmethod
    async def create(self, championship: Championship) -> Championship:
        pass

    @abstractmethod
    async def update(self, championship: Championship) -> Championship:
        pass

    @abstractmethod
    async def delete(self, championship_id: int) -> None:
        pass

    @abstractmethod
    def list_active(self, limit: int, offset: int, user_id: int) -> List[Championship]:
        pass

    @abstractmethod
    def list_next(self, limit: int, offset: int, user_id: int) -> List[Championship]:
        pass

    @abstractmethod
    def count_by_status(self, status: str, user_id: int) -> int:
        pass

    @abstractmethod
    def list_with_user_team(self,
                            user_id: int,
                            status: str | None = None,
                            type: str | None = None,
                            limit: int = 100,
                            offset: int = 0,
                            ) -> List[Tuple[Championship, Team | None]]:
        pass
