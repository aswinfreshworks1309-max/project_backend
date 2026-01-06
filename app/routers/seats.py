from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(
    prefix="/seats", 
    tags=["Seats"],
    dependencies=[Depends(auth.get_current_user)]
)

@router.post("/", response_model=schemas.Seat)
def create_seat(seat: schemas.SeatCreate, db: Session = Depends(get_db)):
    db_seat = models.Seat(**seat.dict())
    db.add(db_seat)
    db.commit()
    db.refresh(db_seat)
    return db_seat

@router.get("/", response_model=List[schemas.Seat])
def read_seats(skip: int = 0, limit: int = 100, bus_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Seat)
    if bus_id:
        query = query.filter(models.Seat.bus_id == bus_id)
        seats = query.offset(skip).limit(limit).all()
        
        # Lazy Initialization: If bus exists but has no seats, create them
        if not seats:
             # Check if bus exists
             bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
             if bus and bus.total_seats > 0:
                 new_seats = []
                 for i in range(bus.total_seats):
                     # Logic: 4 seats per row (A, B, C, D)
                     # i=0 -> 1A, i=1 -> 1B, i=2 -> 1C, i=3 -> 1D, i=4 -> 2A ...
                     row = (i // 4) + 1
                     col_idx = i % 4
                     col_char = chr(65 + col_idx) # 65 is 'A'
                     label = f"{row}{col_char}"
                     
                     seat = models.Seat(bus_id=bus.id, seat_label=label, is_available=True)
                     new_seats.append(seat)
                 
                 db.add_all(new_seats)
                 db.commit()
                 
                 # Refetch seats
                 seats = db.query(models.Seat).filter(models.Seat.bus_id == bus_id).all()
        
        return seats
        
    seats = query.offset(skip).limit(limit).all()
    return seats


@router.post("/reset/{schedule_id}")
def reset_seats(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # 1. Delete all bookings for this schedule
    db.query(models.Booking).filter(models.Booking.schedule_id == schedule_id).delete()
    
    # 2. Reset seat availability for the bus
    db.query(models.Seat).filter(models.Seat.bus_id == schedule.bus_id).update({"is_available": True})
    
    db.commit()
    return {"message": "Seats and bookings reset successfully"}

    
