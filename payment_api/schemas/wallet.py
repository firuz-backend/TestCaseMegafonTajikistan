from pydantic import BaseModel, Field


class WalletSchema(BaseModel):
    id: int
    balance: float


class WalletTopUp(BaseModel):
    amount: float = Field(..., gt=0)
