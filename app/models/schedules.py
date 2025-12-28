from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from app.database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"))
    route_id = Column(String) # Simplified from separate Route model if it existed
    source = Column(String)
    destination = Column(String)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    price = Column(Float)
    available_seats = Column(Integer)
    status = Column(String, default="Scheduled")
