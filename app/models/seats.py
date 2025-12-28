from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database import Base

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"))
    seat_label = Column(String)
    is_available = Column(Boolean, default=True)
