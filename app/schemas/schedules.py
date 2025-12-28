from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ScheduleBase(BaseModel):
    bus_id: int
    route_id: str
    source: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    available_seats: int
    status: Optional[str] = "Scheduled"

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int

    class Config:
        orm_mode = True
