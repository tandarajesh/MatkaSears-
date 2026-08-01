from pydantic import BaseModel


class PrizeMultiplierCreate(BaseModel):
    bet_type: str
    multiplier: int


class PrizeMultiplierUpdate(BaseModel):
    bet_type: str
    multiplier: int


class PrizeMultiplierResponse(BaseModel):
    id: int
    bet_type: str
    multiplier: int

    class Config:
        from_attributes = True