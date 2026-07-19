from datetime import date
from pydantic import BaseModel


class ResultCreate(BaseModel):
    game_id: int
    result_date: date
    open_result: str
    close_result: str


class ResultUpdate(BaseModel):
    game_id: int
    result_date: date
    open_result: str
    close_result: str


class ResultResponse(BaseModel):
    id: int
    game_id: int
    result_date: date
    open_result: str
    close_result: str

    class Config:
        from_attributes = True