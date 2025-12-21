# app/application/championship/use_cases.py

from datetime import datetime
from app.api.championship.schemas import ChampionshipResponse, CreateChampionshipDTO, CreateChampionshipRequest, DashboardStats, TeamDashboardResponse, UpdateChampionshipDTO
from app.application.mappers import to_domain, to_schema
from app.domain.championship.entities import Championship
from app.domain.championship.exceptions import ChampionshipNotFoundException
from app.domain.championship.repositories import IChampionshipRepository
from app.domain.championship.value_objects import ChampionshipStatus, ChampionshipStatusEnum, ChampionshipType
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

        active = self.championship_repo.list_active(
            user_id=self.current_user_id)
        nexts = self.championship_repo.list_next(user_id=self.current_user_id)

        stats = DashboardStats(
            active=active_count,
            finished=finished_count,
            total=total_count
        )

        return TeamDashboardResponse(
            stats=stats,
            active_championships=[
                to_schema(ch, ChampionshipResponse) for ch in active],
            next_championships=[
                to_schema(ch, ChampionshipResponse) for ch in nexts]
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


class GetPaginatedChampionshipsForUserUseCase:
    def __init__(self, championship_repo: IChampionshipRepository):
        self.championship_repo = championship_repo

    def execute(self,
                user_id: int,
                status: str | None = None,
                type: str | None = None,
                limit: int = 100,
                offset: int = 0,
                ):
        championships_with_team = self.championship_repo.list_with_user_team(
            user_id=user_id,
            status=status,
            type=type,
            limit=limit,
            offset=offset,
        )

        return [
            self.to_schema(championship, team)
            for championship, team in championships_with_team
        ]

    def to_schema(self, championship, team):
        response = to_schema(championship, ChampionshipResponse)

        response.is_registered = team is not None
        response.my_team_id = team.id if team else None
        response.can_register = (
            championship.status.value == ChampionshipStatusEnum.INSCRIPTIONS_OPEN.value
            and team is None
        )

        return response


class GetChampionshipByIdUseCase:
    def __init__(self, championship_repo: IChampionshipRepository):
        self.championship_repo = championship_repo

    def execute(self, championship_id: int):
        championship = self.championship_repo.get_by_id(championship_id)
        if not championship:
            raise ChampionshipNotFoundException('Campeonato no encontrado')
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
            type=ChampionshipType(dto.type),
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
    def __init__(self,
                 championship_repo: IChampionshipRepository,
                 file_service: ChampionshipFileService
                 ):
        self.championship_repo = championship_repo
        self.file_service = file_service

    async def execute(self,
                      updated_championship: UpdateChampionshipDTO,
                      championship_id: int,
                      organizer_id: int
                      ) -> ChampionshipResponse:
        existing_championship = self.championship_repo.get_by_id(
            championship_id)
        if not existing_championship:
            raise ChampionshipNotFoundException('Campeonato no encontrado')

        temp_logo_path = None

        try:
            new_domain_championship = to_domain(
                updated_championship, Championship)

            # aqui iria la logica para mergear ambos Championships de domain
            existing_championship = merge_championship(
                existing_championship, new_domain_championship)

            existing_championship.organizer_id = organizer_id

            if updated_championship.logo:
                temp_logo_path = await self.file_service.save_temp_logo(updated_championship.logo)
                final_name = await self.file_service.commit_logo(temp_logo_path)
                existing_championship.logo_url = f"/media/championships/{final_name}"

            updated = self.championship_repo.update(existing_championship)

            return to_schema(updated, ChampionshipResponse)

        except Exception:
            if temp_logo_path:
                await self.file_service.delete_temp(temp_logo_path)
            raise


class DeleteChampionshipUseCase:
    def __init__(self, championship_repo: IChampionshipRepository):
        self.championship_repo = championship_repo

    def execute(self, championship_id: int):
        championship = self.championship_repo.get_by_id(championship_id)
        if not championship:
            raise ChampionshipNotFoundException('Campeonato no encontrado')

        result = self.championship_repo.delete(championship_id)
        if not result:
            return True

        return False


def merge_championship(
    existing: Championship,
    incoming: Championship
) -> Championship:

    # ⚠️ campos que NO se deben tocar nunca
    IMMUTABLE_FIELDS = {
        "id",
        "created_at",
        "teams",
        "organizer",
    }

    for field_name in existing.__dataclass_fields__.keys():
        if field_name in IMMUTABLE_FIELDS:
            continue

        new_value = getattr(incoming, field_name, None)

        # ⚠️ si el mapper no pudo construir el valor → ignorar
        if new_value is None:
            continue

        setattr(existing, field_name, new_value)

    # ⏱️ update automático
    existing.updated_at = datetime.now()

    return existing
