from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    balance = Column(Integer, default=0)

    user = relationship("User", back_populates="wallet")