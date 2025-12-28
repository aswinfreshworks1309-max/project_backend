from pydantic import BaseModel
from typing import Optional

class BusBase(BaseModel):
    bus_number: str
    plate_number: str
    bus_type: str
    total_seats: int
    operator_name: str

class BusCreate(BusBase):
    pass

class Bus(BusBase):
    id: int

    class Config:
        orm_mode = True
