# app/infrastructure/user/sqlalchemy_user_model.py

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime
from app.infrastructure.database import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default='player')
    avatar_url = Column(String, nullable=True)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
