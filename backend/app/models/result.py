from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)

    game_id = Column(Integer, ForeignKey("games.id"))

    result_date = Column(Date, nullable=False)

    open_result = Column(String, nullable=False)

    close_result = Column(String, nullable=False)

    game = relationship("Game", back_populates="results")