from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(
    prefix="/payments", 
    tags=["Payments"],
    dependencies=[Depends(auth.get_current_user)]
)

@router.post("/", response_model=schemas.Payment)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/", response_model=List[schemas.Payment])
def read_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    payments = db.query(models.Payment).offset(skip).limit(limit).all()
    return payments
