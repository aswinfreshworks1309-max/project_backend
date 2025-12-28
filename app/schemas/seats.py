from pydantic import BaseModel
from typing import Optional

class SeatBase(BaseModel):
    bus_id: int
    seat_label: str
    is_available: bool = True

class SeatCreate(SeatBase):
    pass

class Seat(SeatBase):
    id: int

    class Config:
        orm_mode = True
