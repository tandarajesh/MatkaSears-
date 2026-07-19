from datetime import date
from pydantic import BaseModel


class BetCreate(BaseModel):
    user_id: int
    market_id: int
    game_id: int
    bet_type: str
    number: str
    points: int
    bet_date: date


class BetUpdate(BaseModel):
    user_id: int
    market_id: int
    game_id: int
    bet_type: str
    number: str
    points: int
    bet_date: date
    status: str


class BetResponse(BaseModel):
    id: int
    user_id: int
    market_id: int
    game_id: int
    bet_type: str
    number: str
    points: int
    bet_date: date
    status: str

    class Config:
        from_attributes = True