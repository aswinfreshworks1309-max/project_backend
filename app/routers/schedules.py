from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(
    prefix="/schedules", 
    tags=["Schedules"]
)

# Recap: Creates a new travel schedule.
@router.post("/", response_model=schemas.Schedule)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = models.Schedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

from typing import Optional

# Recap: Retrieves schedules, optionally filtered by source and destination.
# Need to recap Again
@router.get("/", response_model=List[schemas.Schedule])
def read_schedules(skip: int = 0, limit: int = 100, source: Optional[str] = None, destination: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Schedule)
    if source:
        query = query.filter(models.Schedule.source.ilike(f"%{source}%"))
    if destination:
        query = query.filter(models.Schedule.destination.ilike(f"%{destination}%"))
    schedules = query.offset(skip).limit(limit).all()
    return schedules


# Recap: Retrieves specific schedule details by ID.
@router.get("/{schedule_id}", response_model=schemas.Schedule)
def read_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

# Recap: Updates an existing schedule's information.
@router.put("/{schedule_id}", response_model=schemas.Schedule)
def update_schedule(schedule_id: int, schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    for key, value in schedule.dict().items():
        setattr(db_schedule, key, value)
    
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

# Recap: Deletes a schedule and its related bookings, and resets bus seats.
@router.delete("/{schedule_id}", status_code=204)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    # Check if schedule exists
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # 1. Delete associated bookings (Fixes ForeignKeyViolation)
    db.query(models.Booking).filter(models.Booking.schedule_id == schedule_id).delete(synchronize_session=False)

    # 2. Reset associated seats to available
    if db_schedule.bus_id:
        db.query(models.Seat).filter(models.Seat.bus_id == db_schedule.bus_id).update({"is_available": True}, synchronize_session=False)

    # 3. Delete the schedule using query to ensure immediate execution order
    db.query(models.Schedule).filter(models.Schedule.id == schedule_id).delete(synchronize_session=False)
    
    db.commit()
    return None
