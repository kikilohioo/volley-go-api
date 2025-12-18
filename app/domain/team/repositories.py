from abc import ABC, abstractmethod
from typing import List
from .entities import Team


class ITeamRepository(ABC):
    @abstractmethod
    async def get_by_id(self, championship_id: int) -> Team | None:
        pass
    
    @abstractmethod
    async def get_by_join_code(self, join_code: int) -> Team | None:
        pass

    @abstractmethod
    async def list(
        self,
        status: str | None = None,
        type: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Team]:
        """Retorna varios campeonatos filtrando por status o tipo, con paginación"""
        pass

    @abstractmethod
    async def create(self, championship: Team) -> Team:
        pass

    @abstractmethod
    async def update(self, championship: Team) -> Team:
        pass

    @abstractmethod
    async def delete(self, championship_id: int) -> None:
        pass