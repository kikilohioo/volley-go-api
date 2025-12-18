# app/infrastructure/teams/sqlalchemy_repository.py

from typing import List
from sqlalchemy.orm import Session
from app.domain.player.entities import Player
from app.domain.player.repositories import IPlayerRepository
from app.domain.player.entities import Player
from .sqlalchemy_player_model import PlayerModel
from app.infrastructure.mappers import to_domain, to_model
from sqlalchemy import func, select
from sqlalchemy import select, exists as sql_exists


class SQLAlchemyPlayerRepository(IPlayerRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, team_id: int) -> Player | None:
        model = self.session.get(PlayerModel, team_id)
        return to_domain(model, Player) if model else None

    def list(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Player]:
        stmt = (
            select(PlayerModel)
            .limit(limit)
            .offset(offset)
        )

        models = self.session.execute(stmt).scalars().all()
        return [to_domain(model, Player) for model in models]

    ####### Commands ######

    def create(self, team: Player) -> Player:
        model = to_model(team, PlayerModel)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return to_domain(model, Player)

    def update(self, team: Player) -> Player:
        model = to_model(team, PlayerModel)
        merged = self.session.merge(model)
        self.session.commit()
        self.session.refresh(merged)
        return to_domain(merged, Player)

    def delete(self, team_id: int) -> None:
        model = self.session.get(PlayerModel, team_id)
        if not model:
            return

        self.session.delete(model)
        self.session.commit()
        
    def exists(self, user_id: int, team_id: int) -> bool:
        stmt = (
            select(
                sql_exists().where(
                    PlayerModel.user_id == user_id,
                    PlayerModel.team_id == team_id,
                )
            )
        )

        exist = self.session.execute(stmt).scalar()
        return exist