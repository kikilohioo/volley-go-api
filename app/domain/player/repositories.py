from abc import ABC, abstractmethod
from typing import List
from .entities import Player


from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Player


class IPlayerRepository(ABC):

    @abstractmethod
    def get_by_id(self, player_id: int) -> Optional[Player]:
        pass

    @abstractmethod
    def list(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Player]:
        pass

    @abstractmethod
    def create(self, player: Player) -> Player:
        pass

    @abstractmethod
    def delete(self, player_id: int) -> None:
        pass

    # 🔍 Validación clave para JoinTeamByCodeUseCase
    @abstractmethod
    def exists(self, user_id: int, team_id: int) -> bool:
        pass

    # (opcional, pero muy útil)
    # @abstractmethod
    # def get_by_user_and_team(
    #     self,
    #     user_id: int,
    #     team_id: int,
    # ) -> Optional[Player]:
    #     pass