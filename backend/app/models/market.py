from sqlalchemy import Column, Integer, String, Boolean

from app.db.database import Base


class Market(Base):
    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, nullable=False)

    open_time = Column(String, nullable=False)

    close_time = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)