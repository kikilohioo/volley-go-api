# app/api/auth/routes.py

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile, Query, status

from app.api.auth.dependencies import get_current_user
from app.api.team.dependencies import get_repo
from app.api.team.schemas import (
    TeamResponse,
    CreateTeamDTO,
    TeamDashboardResponse,
    UpdateTeamDTO,
)
from app.application.team.use_cases import (
    CreateTeamUseCase,
    DeleteTeamUseCase,
    GetTeamByIdUseCase,
    GetPaginatedTeamsUseCase,
    UpdateTeamUseCase,
    TeamDashboardUseCase,
)
from app.infrastructure.file_service import TeamFileService


router = APIRouter(prefix='/teams', tags=['Teams'])


@router.get("/", response_model=list[TeamResponse])
async def get_paginated_teams(limit: int = Query(10, ge=1),
                              offset: int = Query(0, ge=0),
                              repo=Depends(get_repo),
                              current_user=Depends(get_current_user),
                              ):
    use_case = GetPaginatedTeamsUseCase(repo)
    return use_case.execute(limit=limit, offset=offset)


@router.get(
    "/{team_id}/dashboard",
    response_model=TeamDashboardResponse,
)
async def team_dashboard(team_id: int, repo=Depends(get_repo),
                         current_user=Depends(get_current_user),
                         ):
    use_case = TeamDashboardUseCase(repo)
    return use_case.execute(team_id=team_id)


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team_by_id(team_id: int,
                         repo=Depends(get_repo),
                         current_user=Depends(get_current_user),
                         ):
    use_case = GetTeamByIdUseCase(repo)
    return use_case.execute(team_id)


@router.post("/",
             response_model=TeamResponse,
             status_code=status.HTTP_201_CREATED,
             )
async def create_team(request: Request,
                      name: str = Form(...),
                      championship_id: int = Form(...),
                      logo: UploadFile | None = File(None),
                      repo=Depends(get_repo),
                      current_user=Depends(get_current_user),
                      file_service: TeamFileService = Depends(TeamFileService),
                      ):
    print(request.headers.get("authorization"))
    dto = CreateTeamDTO(
        name=name,
        championship_id=championship_id,
        logo=logo,
    )

    use_case = CreateTeamUseCase(repo, file_service)
    new_team = await use_case.execute(dto, user_id=current_user.id)
    return new_team


@router.put(
    "/{team_id}",
    response_model=TeamResponse,
)
async def update_team(team_id: int,
                      name: str = Form(...),
                      championship_id: int = Form(...),
                      logo: UploadFile | None = File(None),
                      repo=Depends(get_repo),
                      current_user=Depends(get_current_user),
                      file_service: TeamFileService = Depends(TeamFileService),
                      ):
    dto = UpdateTeamDTO(
        name=name,
        championship_id=championship_id,
        logo=logo,
    )

    use_case = UpdateTeamUseCase(repo, file_service)
    return await use_case.execute(
        dto=dto,
        team_id=team_id,
        user_id=current_user.id,
    )


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: int,
                      repo=Depends(get_repo),
                      current_user=Depends(get_current_user),
                      ):
    use_case = DeleteTeamUseCase(repo)
    use_case.execute(team_id)
    return None
