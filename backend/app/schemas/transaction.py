from datetime import datetime
from pydantic import BaseModel


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    transaction_type: str
    amount: int
    balance_after: int
    description: str
    created_at: datetime

    class Config:
        from_attributes = True