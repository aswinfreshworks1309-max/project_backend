from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookingBase(BaseModel):
    user_id: int
    schedule_id: int
    seat_id: int
    status: str = "confirmed"

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    booking_date: datetime

    class Config:
        orm_mode = True
