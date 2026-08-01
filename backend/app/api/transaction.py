from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionResponse


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.get(
    "/user/{user_id}",
    response_model=list[TransactionResponse]
)
def get_user_transactions(
    user_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).order_by(
        Transaction.created_at.desc()
    ).all()