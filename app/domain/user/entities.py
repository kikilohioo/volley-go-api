
# app/domain/user/entities.py

from dataclasses import dataclass, field
from datetime import datetime
from app.domain.user.value_objects import UserEmail, UserPassword, UserRole, UserRoleTypeEnum


@dataclass
class User:
    email: UserEmail
    password: UserPassword
    full_name: str
    role: UserRole = field(default_factory=lambda: UserRole("player"))
    id: int | None = None
    avatar_url: str | None = None
    status: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
