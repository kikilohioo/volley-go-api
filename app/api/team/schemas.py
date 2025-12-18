from datetime import datetime
from typing import List, Optional

from fastapi import UploadFile
from pydantic import BaseModel

from app.api.user.schemas import UserResponse

class TeamResponse(BaseModel):
    id: int
    name: str
    logo_url: Optional[str]

    wins: int
    losses: int
    points: int
    sets_won: int
    sets_lost: int

    user: UserResponse
    championship_id: int

    created_at: datetime
    updated_at: datetime
    

class CreateTeamRequest(BaseModel):
    name: str
    championship_id: int
    

class CreateTeamDTO(BaseModel):
    name: str
    championship_id: int
    logo: UploadFile | None = None


class UpdateTeamDTO(BaseModel):
    name: str
    championship_id: int
    logo: UploadFile | None = None
    
    
class DashboardStats(BaseModel):
    total: int
    active: int
    inactive: int
    
    
class TeamDashboardResponse(BaseModel):
    stats: DashboardStats
    # teams: List[TeamResponse] TODO: reemplazar por players list