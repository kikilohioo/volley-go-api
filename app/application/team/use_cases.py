# app/application/team/use_cases.py

import secrets
import string
from app.api.player.schemas import JoinTeamRequest
from app.api.team.schemas import (
    TeamDashboardResponse,
    TeamResponse,
    CreateTeamDTO,
    CreateTeamRequest,
    DashboardStats,
    TeamDashboardResponse,
    UpdateTeamDTO,
)
from app.application.mappers import to_domain, to_schema
from app.domain.player.entities import Player
from app.domain.player.repositories import IPlayerRepository
from app.domain.team.entities import Team
from app.domain.team.exceptions import TeamNotFoundException
from app.domain.team.repositories import ITeamRepository
from app.infrastructure.file_service import TeamFileService


class GetPaginatedTeamsUseCase:
    def __init__(self, team_repo: ITeamRepository):
        self.team_repo = team_repo

    def execute(self, limit: int = 100, offset: int = 0):
        teams = self.team_repo.list(limit=limit, offset=offset)
        return [to_schema(team, TeamResponse) for team in teams]


class GetTeamByIdUseCase:
    def __init__(self, team_repo: ITeamRepository):
        self.team_repo = team_repo

    def execute(self, team_id: int):
        team = self.team_repo.get_by_id(team_id)
        if not team:
            raise TeamNotFoundException("Team not found")

        return to_schema(team, TeamResponse)


class CreateTeamUseCase:
    def __init__(
        self,
        team_repo: ITeamRepository,
        player_repo: IPlayerRepository,
        file_service: TeamFileService,
    ):
        self.team_repo = team_repo
        self.player_repo = player_repo
        self.file_service = file_service

    async def execute(self, dto: CreateTeamDTO, new_player: JoinTeamRequest, user_id: int):
        # 1. Crear entidad de dominio
        team = Team(
            name=dto.name,
            championship_id=dto.championship_id,
            user_id=user_id,
            join_code=self.generate_team_code()
        )

        # 2. Procesar logo
        if dto.logo:
            temp_path = await self.file_service.save_temp_logo(dto.logo)
            final_name = await self.file_service.commit_logo(temp_path)
            team.logo_url = f"/media/teams/{final_name}"

        # 3. Persistir
        created = self.team_repo.create(team)
        
        player = Player(
            user_id=user_id,
            team_id=created.id,
            position=new_player.position,
            jersey_number=new_player.jersey_number
        )
        
        self.player_repo.create(player)
        
        return to_schema(created, TeamResponse)
        
    def generate_team_code(self, length: int = 6) -> str:
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))


class UpdateTeamUseCase:
    def __init__(
        self,
        team_repo: ITeamRepository,
        file_service: TeamFileService,
    ):
        self.team_repo = team_repo
        self.file_service = file_service

    async def execute(
        self,
        dto: UpdateTeamDTO,
        team_id: int,
        user_id: int,
    ) -> TeamResponse:

        team = self.team_repo.get_by_id(team_id)
        if not team:
            raise TeamNotFoundException("Team not found")

        # 🔐 ownership (opcional pero recomendado)
        if team.user_id != user_id:
            raise TeamNotFoundException("Team not found")

        # 📝 actualizar campos
        team.name = dto.name
        team.championship_id = dto.championship_id
        team.user_id = user_id

        # 🖼️ actualizar logo (opcional)
        if dto.logo:
            temp_path = await self.file_service.save_temp_logo(dto.logo)
            final_name = await self.file_service.commit_logo(temp_path)
            team.logo_url = f"/media/teams/{final_name}"

        updated = self.team_repo.update(team)
        return to_schema(updated, TeamResponse)


class DeleteTeamUseCase:
    def __init__(self, team_repo: ITeamRepository):
        self.team_repo = team_repo

    def execute(self, team_id: int):
        team = self.team_repo.get_by_id(team_id)
        if not team:
            raise TeamNotFoundException("Team not found")

        self.team_repo.delete(team_id)
        return True


class TeamDashboardUseCase:
    def __init__(self, team_repo: ITeamRepository):
        self.team_repo = team_repo

    def execute(self, team_id: int):
        team = self.team_repo.get_by_id(team_id)
        if not team:
            raise TeamNotFoundException("Team not found")

        return TeamDashboardResponse(
            stats=team.stats
        )
