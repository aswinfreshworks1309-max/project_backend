from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    booking_id: int
    amount: float
    transaction_id: str
    status: str = "pending"

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
