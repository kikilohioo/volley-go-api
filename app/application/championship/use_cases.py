# app/application/championship/use_cases.py

from datetime import datetime
from app.api.championship.schemas import ChampionshipResponse, CreateChampionshipDTO, CreateChampionshipRequest, DashboardStats, OrganizerDashboardResponse
from app.application.mappers import to_domain, to_schema
from app.domain.championship.entities import Championship
from app.domain.championship.exceptions import ChampionshipNotFoundException
from app.domain.championship.repositories import IChampionshipRepository
from app.domain.championship.value_objects import ChampionshipStatusEnum
from app.infrastructure.file_service import ChampionshipFileService


class GetDashboardUseCase:
    def __init__(self, championship_repo: IChampionshipRepository, current_user_id: int):
        self.championship_repo = championship_repo
        self.current_user_id = current_user_id

    def execute(self):
        active_count = self.championship_repo.count_by_status(
            status=ChampionshipStatusEnum.ONGOING.value, user_id=self.current_user_id)
        finished_count = self.championship_repo.count_by_status(
            status=ChampionshipStatusEnum.COMPLETED.value, user_id=self.current_user_id)
        total_count = active_count + finished_count

        active = self.championship_repo.list_active(user_id=self.current_user_id)
        nexts = self.championship_repo.list_next(user_id=self.current_user_id)

        stats = DashboardStats(
            active=active_count,
            finished=finished_count,
            total=total_count
        )

        return OrganizerDashboardResponse(
            stats=stats,
            active_championships=[to_schema(ch, ChampionshipResponse) for ch in active],
            next_championships=[to_schema(ch, ChampionshipResponse) for ch in nexts]
        )


class GetPaginatedChampionshipsUseCase:
    def __init__(self, championship_repo: IChampionshipRepository):
        self.championship_repo = championship_repo

    def execute(self, status: str | None = None, type: str | None = None, limit: int = 100, offset: int = 0):
        filtered_championships = self.championship_repo.list(
            status=status, type=type, limit=limit, offset=offset)

        return self.to_schema(filtered_championships)

    def to_schema(self, filtered_championships):
        return [to_schema(champ, ChampionshipResponse) for champ in filtered_championships]


class GetChampionshipByIdUseCase:
    def __init__(self, championship_repo: IChampionshipRepository):
        self.championship_repo = championship_repo

    def execute(self, championship_id: int):
        championship = self.championship_repo.get_by_id(championship_id)
        if not championship:
            raise ChampionshipNotFoundException('Championship not found')
        return to_schema(championship, ChampionshipResponse)


class CreateChampionsipUseCase:
    def __init__(self, championship_repo: IChampionshipRepository, file_service: ChampionshipFileService):
        self.championship_repo = championship_repo
        self.file_service = file_service

    async def execute(self, dto: CreateChampionshipDTO, organizer_id: int) -> Championship:
        
        # 1. Crear objeto dominio
        championship = Championship(
            name=dto.name,
            location=dto.location,
            type=dto.type,
            sets_to_win=dto.sets_to_win,
            points_per_set=dto.points_per_set,
            start_date=dto.start_date,
            end_date=dto.end_date,
            player_cost=dto.player_cost,
            description=dto.description,
            max_teams=dto.max_teams,
            organizer_id=organizer_id
        )

        # 2. Procesar logo si viene
        if dto.logo:
            temp_path = await self.file_service.save_temp_logo(dto.logo)
            final_name = await self.file_service.commit_logo(temp_path)
            championship.logo_url = f"/media/championships/{final_name}"

        # 3. Persistir
        created = self.championship_repo.create(championship)
        return to_schema(created, ChampionshipResponse)


class UpdateChampionsipUseCase:
    def __init__(self, championship_repo: IChampionshipRepository):
        self.championship_repo = championship_repo

    def execute(self, updated_championship: CreateChampionshipRequest,
                championship_id: int, organizer_id: int) -> Championship:
        championship = to_domain(updated_championship, Championship)

        championship.id = championship_id
        championship.organizer_id = organizer_id

        created_championship = self.championship_repo.update(championship)
        return to_schema(created_championship, ChampionshipResponse)


class DeleteChampionshipUseCase:
    def __init__(self, championship_repo: IChampionshipRepository):
        self.championship_repo = championship_repo

    def execute(self, championship_id: int):
        championship = self.championship_repo.get_by_id(championship_id)
        if not championship:
            raise ChampionshipNotFoundException('Championship not found')

        result = self.championship_repo.delete(championship_id)
        if not result:
            return True

        return False
