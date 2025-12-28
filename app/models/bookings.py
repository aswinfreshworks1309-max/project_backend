from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    schedule_id = Column(Integer, ForeignKey("schedules.id"))
    seat_id = Column(Integer, ForeignKey("seats.id"))
    booking_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="confirmed")
