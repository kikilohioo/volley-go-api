# app/infrastructure/championship/sqlalchemy_championship_model.py

from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.database import Base


class TeamModel(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)

    # --- Basic info ---
    name = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)
    join_code = Column(String, nullable=False)

    # --- Stats ---
    wins = Column(Integer, nullable=False, default=0)
    losses = Column(Integer, nullable=False, default=0)
    points = Column(Integer, nullable=False, default=0)
    sets_won = Column(Integer, nullable=False, default=0)
    sets_lost = Column(Integer, nullable=False, default=0)

    # --- Relations ---
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship('UserModel')
    championship_id = Column(Integer, ForeignKey("championships.id"), nullable=False)
    championship = relationship('ChampionshipModel')
    players = relationship("PlayerModel", back_populates="team", cascade="all, delete-orphan")

    # --- Metadata ---
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )
