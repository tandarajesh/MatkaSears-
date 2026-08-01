from datetime import date
from pydantic import BaseModel


class ResultCreate(BaseModel):
    market_id: int
    game_id: int
    result_date: date
    open_result: str
    close_result: str


class ResultUpdate(BaseModel):
    market_id: int
    game_id: int
    result_date: date
    open_result: str
    close_result: str


class ResultResponse(BaseModel):
    id: int
    market_id: int
    game_id: int
    result_date: date
    open_result: str
    close_result: str

    class Config:
        from_attributes = True