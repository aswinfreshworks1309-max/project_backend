from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(
    prefix="/buses", 
    tags=["Buses"],
    dependencies=[Depends(auth.get_current_user)]
)

@router.post("/", response_model=schemas.Bus)
def create_bus(bus: schemas.BusCreate, db: Session = Depends(get_db)):
    db_bus = models.Bus(**bus.dict())
    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)
    return db_bus

@router.get("/", response_model=List[schemas.Bus])
def read_buses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    buses = db.query(models.Bus).offset(skip).limit(limit).all()
    return buses

@router.get("/{bus_id}", response_model=schemas.Bus)
def read_bus(bus_id: int, db: Session = Depends(get_db)):
    bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if bus is None:
        raise HTTPException(status_code=404, detail="Bus not found")
    return bus
