from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    market_id = Column(Integer, ForeignKey("markets.id"))
    game_id = Column(Integer, ForeignKey("games.id"))

    bet_type = Column(String, nullable=False)
    number = Column(String, nullable=False)
    points = Column(Integer, nullable=False)

    bet_date = Column(Date, nullable=False)

    status = Column(String, default="Pending")

    user = relationship("User", back_populates="bets")
    market = relationship("Market", back_populates="bets")
    game = relationship("Game", back_populates="bets")