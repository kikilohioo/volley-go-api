# app/infrastructure/user/sqlalchemy_repository.py

from sqlalchemy.orm import Session
from app.domain.user.repositories import IUserRepository
from app.domain.user.entities import User
from app.infrastructure.mappers import to_domain, to_model
from .sqlalchemy_user_model import UserModel
from sqlalchemy import select


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> User | None:
        model = self.session.get(UserModel, user_id)
        return to_domain(model, User) if model else None

    def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return to_domain(model, User) if model else None

    def create(self, user: User) -> User:
        model = to_model(user, UserModel)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return to_domain(model, User)

    def update(self, user: User) -> User:
        model = to_model(user, UserModel)
        merged = self.session.merge(model)
        self.session.commit()
        self.session.refresh(merged)
        return to_domain(merged, User)
    
    def delete(self, user_id: int) -> None:
        model = self.session.get(UserModel, user_id)
        if model:
            self.session.delete(model)
            self.session.commit()
