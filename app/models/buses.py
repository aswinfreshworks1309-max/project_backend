from sqlalchemy import Column, Integer, String
from app.database import Base

class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    bus_number = Column(String, unique=True, index=True)
    plate_number = Column(String, unique=True)
    bus_type = Column(String)
    total_seats = Column(Integer)
    operator_name = Column(String)
