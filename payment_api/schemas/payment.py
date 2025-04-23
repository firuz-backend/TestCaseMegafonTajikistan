from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentCreate(BaseModel):
    service_id: int


class PaymentResponse(BaseModel):
    payment_id: int
    status: str
    balance_after: Optional[float]


class PaymentStatus(BaseModel):
    payment_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
