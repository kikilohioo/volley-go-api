# app/domain/user/repositories.py

from abc import ABC, abstractmethod
from .entities import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass
    
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def delete(self, user_id: int) -> None:
        pass

