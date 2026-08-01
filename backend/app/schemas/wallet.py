from pydantic import BaseModel


class WalletCreate(BaseModel):
    user_id: int


class WalletUpdate(BaseModel):
    balance: int


class WalletResponse(BaseModel):
    id: int
    user_id: int
    balance: int

    class Config:
        from_attributes = True