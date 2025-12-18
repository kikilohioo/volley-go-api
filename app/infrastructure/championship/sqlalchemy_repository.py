# app/infrastructure/championship/sqlalchemy_repository.py

from typing import List
from sqlalchemy.orm import Session
from app.domain.championship.entities import Championship
from app.domain.championship.repositories import IChampionshipRepository
from app.domain.championship.entities import Championship
from app.domain.championship.value_objects import ChampionshipStatusEnum
from app.domain.team.entities import Team
from app.infrastructure.player.sqlalchemy_player_model import PlayerModel
from app.infrastructure.team.sqlalchemy_team_model import TeamModel
from .sqlalchemy_championship_model import ChampionshipModel
from app.infrastructure.mappers import to_domain, to_model
from sqlalchemy import and_, func, select


class SQLAlchemyChampionshipRepository(IChampionshipRepository):
    def __init__(self, session: Session):
        self.session = session

    ####### CRUD ######
    def get_by_id(self, championship_id: int) -> Championship | None:
        model = self.session.get(ChampionshipModel, championship_id)
        return to_domain(model, Championship) if model else None

    def list(
        self,
        status: str | None = None,
        type: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Championship]:
        query = select(ChampionshipModel)

        if status:
            query = query.where(ChampionshipModel.status == status)
        if type:
            query = query.where(ChampionshipModel.type == type)

        query = query.limit(limit).offset(offset)

        result = self.session.execute(query)
        models = result.scalars().all()

        entities = [to_domain(m, Championship) for m in models]
        return entities

    def create(self, championship: Championship) -> Championship:
        model = to_model(championship, ChampionshipModel)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return to_domain(model, Championship)

    def update(self, championship: Championship) -> Championship:
        model = to_model(championship, ChampionshipModel)
        merged = self.session.merge(model)
        self.session.commit()
        self.session.refresh(merged)
        return to_domain(merged, Championship)

    def delete(self, championship_id: int) -> None:
        model = self.session.get(ChampionshipModel, championship_id)
        if model:
            self.session.delete(model)
            self.session.commit()

    def list_active(self,
                    user_id: int,
                    limit: int = 100,
                    offset: int = 0,
                    ) -> List[Championship]:
        query = select(ChampionshipModel) \
            .where(ChampionshipModel.organizer_id == user_id) \
            .where(ChampionshipModel.status == ChampionshipStatusEnum.ONGOING.value)

        query = query.limit(limit).offset(offset)

        result = self.session.execute(query)
        models = result.scalars().all()
        return [to_domain(m, Championship) for m in models]

    def list_next(self,
                  user_id: int,
                  limit: int = 100,
                  offset: int = 0,
                  ) -> List[Championship]:
        query = (
            select(ChampionshipModel)
            .where(ChampionshipModel.organizer_id == user_id)
            .where(
                ChampionshipModel.status.in_([
                    ChampionshipStatusEnum.UPCOMING.value,
                    ChampionshipStatusEnum.INSCRIPTIONS_OPEN.value,
                    ChampionshipStatusEnum.INSCRIPTIONS_CLOSED.value
                ])
            )
            .limit(limit)
            .offset(offset)
        )

        query = query.limit(limit).offset(offset)

        result = self.session.execute(query)
        models = result.scalars().all()
        return [to_domain(m, Championship) for m in models]

    def count_by_status(self, status: str, user_id: int) -> int:
        query = select(func.count()).select_from(ChampionshipModel).where(
            ChampionshipModel.status == status
        ).where(ChampionshipModel.organizer_id == user_id)

        return self.session.execute(query).scalar()

    def list_with_user_team(self,
                            user_id: int,
                            status: str | None = None,
                            type: str | None = None,
                            limit: int = 100,
                            offset: int = 0,
                            ) -> list[tuple[Championship, Team | None]]:

        stmt = (select(ChampionshipModel, TeamModel)
                .outerjoin(
                TeamModel,
                TeamModel.championship_id == ChampionshipModel.id,
                )
                .outerjoin(
                PlayerModel,
                and_(
                    PlayerModel.team_id == TeamModel.id,
                    PlayerModel.user_id == user_id,
                ),
                )
                )

        if status:
            stmt = stmt.where(ChampionshipModel.status == status)

        if type:
            stmt = stmt.where(ChampionshipModel.type == type)

        stmt = stmt.limit(limit).offset(offset)

        result = self.session.execute(stmt).all()

        return [
            (
                to_domain(championship_model, Championship),
                to_domain(team_model, Team) if player_model else None,
            )
            for championship_model, team_model, player_model in
            self.session.execute(
                stmt.add_columns(PlayerModel)
            ).all()
        ]
