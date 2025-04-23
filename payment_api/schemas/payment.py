from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class PaymentCreate(BaseModel):
    service_id: int


class PaymentResponse(BaseModel):
    payment_id: int
    status: str
    amount: Optional[float]


class PaymentStatus(BaseModel):
    payment_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
