from app.api.player.schemas import PlayerResponse
from app.application.mappers import to_domain, to_schema
from app.domain.player.entities import Player
from app.domain.player.exceptions import PlayerAlreadyExistsException
from app.domain.player.repositories import IPlayerRepository
from app.domain.team.entities import Team
from app.domain.team.exceptions import TeamNotFoundException
from app.domain.team.repositories import ITeamRepository


class GetPaginatedPlayersUseCase:
    def __init__(self, player_repo: IPlayerRepository):
        self.player_repo = player_repo

    def execute(self, limit: int = 100, offset: int = 0):
        players = self.player_repo.list(limit=limit, offset=offset)
        return [to_schema(player, PlayerResponse) for player in players]


class GetPlayerByIdUseCase:
    def __init__(self, player_repo: IPlayerRepository):
        self.player_repo = player_repo

    def execute(self, player_id: int):
        player = self.player_repo.get_by_id(player_id)
        if not player:
            raise TeamNotFoundException("Player not found")

        return to_schema(player, PlayerResponse)


class LeaveTeamUseCase:
    def __init__(self, player_repo: IPlayerRepository):
        self.player_repo = player_repo

    def execute(self, player_id: int, user_id: int):
        player = self.player_repo.get_by_id(player_id)
        if not player or player.user_id != user_id:
            raise TeamNotFoundException("Player not found")

        self.player_repo.delete(player_id)
        return True


class JoinTeamByCodeUseCase:
    def __init__(
        self,
        player_repo: IPlayerRepository,
        team_repo: ITeamRepository,
    ):
        self.player_repo = player_repo
        self.team_repo = team_repo

    def execute(
        self,
        user_id: int,
        join_code: str,
        position: str | None = None,
        jersey_number: int | None = None,
    ):
        team = self.team_repo.get_by_join_code(join_code)
        if not team:
            raise TeamNotFoundException("Codigo de equipo invalido")

        if self.player_repo.exists(user_id=user_id, team_id=team.id):
            raise PlayerAlreadyExistsException("User already in this team")

        player = Player(
            user_id=user_id,
            team_id=team.id,
            position=position,
            jersey_number=jersey_number,
        )

        created = self.player_repo.create(player)
        return to_schema(created, PlayerResponse)
