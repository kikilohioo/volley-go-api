# app/infrastructure/championship/sqlalchemy_championship_model.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.database import Base


class PlayerModel(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)

    # --- Relations ---
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)

    user = relationship("UserModel")
    team = relationship("TeamModel", back_populates="players")

    # --- Player info ---
    position = Column(String, nullable=True)
    jersey_number = Column(Integer, nullable=True)

    # --- Metadata ---
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    __table_args__ = (
        UniqueConstraint("user_id", "team_id", name="uq_user_team"),
    )