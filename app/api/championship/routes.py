# app/api/auth/routes.py

from datetime import datetime
from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.params import Query
from app.api.auth.dependencies import get_current_user
from app.api.championship.dependencies import get_repo
from app.application.championship.use_cases import CreateChampionsipUseCase, DeleteChampionshipUseCase, GetChampionshipByIdUseCase, GetDashboardUseCase, GetPaginatedChampionshipsForUserUseCase, GetPaginatedChampionshipsUseCase, UpdateChampionsipUseCase
from app.domain.championship.value_objects import ChampionshipStatusEnum, ChampionshipTypeEnum
from app.infrastructure.file_service import ChampionshipFileService
from .schemas import ChampionshipResponse, CreateChampionshipDTO, CreateChampionshipRequest, TeamDashboardResponse, UpdateChampionshipDTO, UpdateChampionshipRequest


router = APIRouter(prefix='/championships', tags=['Championships'])


@router.get('/', response_model=list[ChampionshipResponse])
async def get_championships(type: ChampionshipTypeEnum | None = Query(None, description="Tipo de campeonato"),
                                      status: ChampionshipStatusEnum | None = Query(
                                          None, description="Estado del campeonato"),
                                      limit: int = Query(
                                          10, description="Número máximo de resultados a obtener"),
                                      offset: int = Query(
                                          0, description="Número de resultados a saltar para paginación"),
                                      repo=Depends(get_repo),  current_user=Depends(get_current_user)):

    use_case = GetPaginatedChampionshipsUseCase(repo)

    championships = use_case.execute(
        status=status, type=type, limit=limit, offset=offset)

    return championships


@router.get(
    "/me",
    response_model=list[ChampionshipResponse],
    summary="Obtener campeonatos con estado de inscripción del usuario"
)
async def get_my_championships(type: ChampionshipTypeEnum | None = Query(
                                    None, description="Tipo de campeonato"
                                ),
                                status: ChampionshipStatusEnum | None = Query(
                                    None, description="Estado del campeonato"
                                ),
                                limit: int = Query(
                                    10, description="Número máximo de resultados a obtener"
                                ),
                                offset: int = Query(
                                    0, description="Número de resultados a saltar para paginación"
                                ),
                                repo=Depends(get_repo),
                                current_user=Depends(get_current_user),
    ):
    use_case = GetPaginatedChampionshipsForUserUseCase(repo)

    championships = use_case.execute(
        user_id=current_user.id,
        status=status,
        type=type,
        limit=limit,
        offset=offset,
    )

    return championships


@router.get('/organizer/dashboard', response_model=TeamDashboardResponse)
async def get_dashboard_championships(type: ChampionshipTypeEnum | None = Query(None, description="Tipo de campeonato"),
                                      status: ChampionshipStatusEnum | None = Query(
                                          None, description="Estado del campeonato"),
                                      limit: int = Query(
                                          10, description="Número máximo de resultados a obtener"),
                                      offset: int = Query(
                                          0, description="Número de resultados a saltar para paginación"),
                                      repo=Depends(get_repo),  current_user=Depends(get_current_user)):
    use_case = GetDashboardUseCase(championship_repo=repo, current_user_id=current_user.id)

    dashboard = use_case.execute()

    return dashboard


@router.get('/{championship_id}', response_model=ChampionshipResponse)
async def get_championships_by_id(championship_id: int, repo=Depends(get_repo), current_user=Depends(get_current_user)):
    use_case = GetChampionshipByIdUseCase(repo)
    championship = use_case.execute(championship_id)

    return championship


@router.post('/', response_model=ChampionshipResponse, status_code=status.HTTP_201_CREATED)
async def create_championship(
    name: str = Form(...),
    location: str = Form(...),
    type: str = Form(...),
    sets_to_win: int = Form(...),
    player_cost: float = Form(...),
    points_per_set: int = Form(...),
    start_date: datetime = Form(...),
    end_date: datetime = Form(...),
    description: str = Form(...),
    max_teams: int = Form(...),
    
    logo: UploadFile | None = File(None),

    repo=Depends(get_repo),
    current_user=Depends(get_current_user),
    file_service: ChampionshipFileService = Depends(ChampionshipFileService)
):

    dto = CreateChampionshipDTO(
        name=name,
        location=location,
        type=type,
        sets_to_win=sets_to_win,
        points_per_set=points_per_set,
        start_date=start_date,
        end_date=end_date,
        player_cost=player_cost,
        description=description,
        max_teams=max_teams,
        logo=logo
    )

    use_case = CreateChampionsipUseCase(repo, file_service)
    return await use_case.execute(dto, organizer_id=current_user.id)


@router.put(
    '/{championship_id}',
    response_model=ChampionshipResponse
)
async def update_championship(
    championship_id: int,

    name: str = Form(...),
    location: str = Form(...),
    type: str = Form(...),
    sets_to_win: int = Form(...),
    points_per_set: int = Form(...),
    player_cost: float = Form(...),
    start_date: datetime = Form(...),
    end_date: datetime = Form(...),
    description: str = Form(...),
    status: str | None = Form(...),
    max_teams: int = Form(...),

    logo: UploadFile | None = File(None),

    repo=Depends(get_repo),
    current_user=Depends(get_current_user),
    file_service: ChampionshipFileService = Depends(ChampionshipFileService)
):

    dto = UpdateChampionshipDTO(
        name=name,
        location=location,
        type=type,
        sets_to_win=sets_to_win,
        points_per_set=points_per_set,
        start_date=start_date,
        end_date=end_date,
        player_cost=player_cost,
        description=description,
        max_teams=max_teams,
        status=status,
        logo=logo
    )

    use_case = UpdateChampionsipUseCase(repo, file_service)

    return await use_case.execute(
        updated_championship=dto,
        championship_id=championship_id,
        organizer_id=current_user.id
    )


@router.delete('/{championship_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_championship(championship_id: int, repo=Depends(get_repo), current_user=Depends(get_current_user)):
    use_case = DeleteChampionshipUseCase(repo)
    championship = use_case.execute(championship_id)
    return championship
