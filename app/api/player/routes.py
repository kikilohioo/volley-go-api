from fastapi import APIRouter, Depends, Query, status

from app.api.auth.dependencies import get_current_user
from app.api.player.dependencies import get_repo
from app.api.team.dependencies import get_repo as get_team_repo
from app.api.player.schemas import (
    PlayerResponse,
    JoinTeamRequest,
)
from app.application.player.use_cases import (
    GetPaginatedPlayersUseCase,
    GetPlayerByIdUseCase,
    JoinTeamByCodeUseCase,
    LeaveTeamUseCase,
)

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("/", response_model=list[PlayerResponse])
async def get_paginated_players(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    repo=Depends(get_repo),
    current_user=Depends(get_current_user),
):
    use_case = GetPaginatedPlayersUseCase(repo)
    return use_case.execute(limit=limit, offset=offset)


@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player_by_id(
    player_id: int,
    repo=Depends(get_repo),
    current_user=Depends(get_current_user),
):
    use_case = GetPlayerByIdUseCase(repo)
    return use_case.execute(player_id)


@router.post(
    "/join-team",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def join_team_by_code(
    request: JoinTeamRequest,
    player_repo=Depends(get_repo),
    team_repo=Depends(get_team_repo),
    current_user=Depends(get_current_user),
):
    use_case = JoinTeamByCodeUseCase(
        player_repo=player_repo,
        team_repo=team_repo,
    )

    return use_case.execute(
        user_id=current_user.id,
        join_code=request.join_code,
        position=request.position,
        jersey_number=request.jersey_number,
    )
    
    
@router.delete(
    "/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def leave_team(
    player_id: int,
    repo=Depends(get_repo),
    current_user=Depends(get_current_user),
):
    use_case = LeaveTeamUseCase(repo)
    use_case.execute(player_id=player_id, user_id=current_user.id)
    return None