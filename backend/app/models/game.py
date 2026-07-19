from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(Integer, ForeignKey("markets.id"))
    name = Column(String, nullable=False)
    open_time = Column(String)
    close_time = Column(String)
    is_active = Column(Boolean, default=True)

    market = relationship("Market", back_populates="games")
    results = relationship("Result", back_populates="game")