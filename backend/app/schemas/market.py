from pydantic import BaseModel


class MarketCreate(BaseModel):
    name: str
    open_time: str
    close_time: str


class MarketUpdate(BaseModel):
    name: str
    open_time: str
    close_time: str
    is_active: bool


class MarketResponse(BaseModel):
    id: int
    name: str
    open_time: str
    close_time: str
    is_active: bool

    class Config:
        from_attributes = True