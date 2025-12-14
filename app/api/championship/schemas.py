# app/api/championship/schemas.py

from datetime import datetime
from typing import List, Optional
from fastapi import UploadFile
from pydantic import BaseModel
from app.api.user.schemas import UserResponse


class ChampionshipResponse(BaseModel):
    id: int
    name: str
    location: Optional[str]
    start_date: datetime
    end_date: datetime
    organizer: UserResponse
    created_at: datetime
    updated_at: datetime
    type: str
    sets_to_win: int
    points_per_set: int
    player_cost: float
    description: Optional[str]
    logo_url: Optional[str]
    max_teams: int
    status: str


class CreateChampionshipRequest(BaseModel):
    name: str
    location: str
    type: str
    sets_to_win: int
    points_per_set: int
    player_cost: float
    start_date: datetime
    end_date: datetime
    description: str
    logo_url: str
    max_teams: int


class UpdateChampionshipRequest(BaseModel):
    name: str
    location: str
    type: str
    sets_to_win: int
    points_per_set: int
    player_cost: float
    start_date: datetime
    end_date: datetime
    description: Optional[str] = None
    logo_url: Optional[str] = None
    max_teams: int


class OrganizerDashboardResponse(BaseModel):
    stats: DashboardStats
    active_championships: List[ChampionshipResponse]
    next_championships: List[ChampionshipResponse]
        
        

class DashboardStats(BaseModel):
    active: int
    finished: int
    total: int


class CreateChampionshipDTO(BaseModel):
    name: str
    location: str
    type: str
    sets_to_win: int
    points_per_set: int
    start_date: datetime
    end_date: datetime
    player_cost: float
    description: str
    max_teams: int
    
    logo: UploadFile | None = None