from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class JoinTeamDTO(BaseModel):
    join_code: str
    position: Optional[str] = None
    jersey_number: Optional[int] = None
    
    
class JoinTeamRequest(BaseModel):
    join_code: str
    position: Optional[str] = None
    jersey_number: Optional[int] = None
    

class PlayerResponse(BaseModel):
    id: int
    user_id: int
    team_id: int

    position: Optional[str]
    jersey_number: Optional[int]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True