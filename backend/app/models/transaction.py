from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    transaction_type = Column(
        String,
        nullable=False
    )

    amount = Column(
        Integer,
        nullable=False
    )

    balance_after = Column(
        Integer,
        nullable=False
    )

    description = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )