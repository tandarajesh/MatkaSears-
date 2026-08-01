from sqlalchemy import Column, Integer, String

from app.db.database import Base


class PrizeMultiplier(Base):
    __tablename__ = "prize_multipliers"

    id = Column(Integer, primary_key=True, index=True)

    bet_type = Column(String, unique=True, nullable=False)

    multiplier = Column(Integer, nullable=False)