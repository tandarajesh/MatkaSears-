from pydantic import BaseModel


class GameCreate(BaseModel):
    market_id: int
    name: str
    open_time: str
    close_time: str


class GameUpdate(BaseModel):
    market_id: int
    name: str
    open_time: str
    close_time: str
    is_active: bool


class GameResponse(BaseModel):
    id: int
    market_id: int
    name: str
    open_time: str
    close_time: str
    is_active: bool

    class Config:
        from_attributes = True