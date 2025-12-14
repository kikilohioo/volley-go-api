# app/infrastructure/championship/sqlalchemy_championship_model.py

from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.database import Base


class ChampionshipModel(Base):
    __tablename__ = 'championships'

    id = Column(Integer, primary_key=True, index=True)
    organizer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    organizer = relationship('UserModel')
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    sets_to_win = Column(Integer, nullable=False)
    points_per_set = Column(Integer, nullable=False)
    player_cost = Column(Float, nullable=False)
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime, default=datetime.now)
    description = Column(String, nullable=True)
    location = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)
    max_teams = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
