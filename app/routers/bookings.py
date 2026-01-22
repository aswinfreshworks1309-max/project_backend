from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(
    prefix="/bookings", 
    tags=["Bookings"],
    dependencies=[Depends(auth.get_current_user)]
)

# Recap: Processes and creates a new booking while marking the seat as unavailable.
@router.post("/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    try:
        # Check if seat is already booked for this schedule
        existing = db.query(models.Booking).filter(
            models.Booking.seat_id == booking.seat_id,
            models.Booking.schedule_id == booking.schedule_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=400, 
                detail=f"Seat {booking.seat_id} is already booked for this schedule"
            )
        
        # Update seat availability
        seat = db.query(models.Seat).filter(models.Seat.id == booking.seat_id).first()
        if seat:
            seat.is_available = False
            db.add(seat)
        
        db_booking = models.Booking(**booking.dict())
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating booking: {str(e)}")

# Recap: Lists bookings with optional filtering by schedule or user.
@router.get("/", response_model=List[schemas.Booking])
def read_bookings(skip: int = 0, limit: int = 100, schedule_id: int = None, user_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Booking)
    if schedule_id:
        query = query.filter(models.Booking.schedule_id == schedule_id)
    if user_id:
        query = query.filter(models.Booking.user_id == user_id)
    bookings = query.offset(skip).limit(limit).all()
    return bookings

# Recap: Retrieves a single booking record by its ID.
@router.get("/{booking_id}", response_model=schemas.Booking)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking
