# app/infrastructure/teams/sqlalchemy_repository.py

from typing import List
from sqlalchemy.orm import Session
from app.domain.team.entities import Team
from app.domain.team.repositories import ITeamRepository
from app.domain.team.entities import Team
from .sqlalchemy_team_model import TeamModel
from app.infrastructure.mappers import to_domain, to_model
from sqlalchemy import func, select


class SQLAlchemyTeamRepository(ITeamRepository):
    def __init__(self, session: Session):
        self.session = session

    ####### CRUD ######
    def get_by_id(self, teams_id: int) -> Team | None:
        model = self.session.get(TeamModel, teams_id)
        return to_domain(model, Team) if model else None
    
    def get_by_join_code(self, join_code: str) -> Team | None:
        stmt = select(TeamModel).where(TeamModel.join_code == join_code)
        model = self.session.execute(stmt).scalar_one_or_none()
        return to_domain(model, Team) if model else None

    def list(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[Team]:
        query = select(TeamModel)
        query = query.limit(limit).offset(offset)

        result = self.session.execute(query)
        models = result.scalars().all()

        entities = [to_domain(m, Team) for m in models]
        return entities

    def create(self, teams: Team) -> Team:
        model = to_model(teams, TeamModel)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return to_domain(model, Team)

    def update(self, teams: Team) -> Team:
        model = to_model(teams, TeamModel)
        merged = self.session.merge(model)
        self.session.commit()
        self.session.refresh(merged)
        return to_domain(merged, Team)

    def delete(self, teams_id: int) -> None:
        model = self.session.get(TeamModel, teams_id)
        if model:
            self.session.delete(model)
            self.session.commit()
