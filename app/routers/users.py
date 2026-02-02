from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import auth

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

# Recap: Creates a new user with hashed password.
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        name=user.name, 
        email=user.email, 
        hashed_password=hashed_password, 
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Recap: Authenticates user via JSON payload and returns token with user info.
@router.post("/login")
def login(user_credentials: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not user or not auth.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Generate token
    access_token = auth.create_access_token(data={"sub": user.email})
    
    # Return user data combined with token
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "access_token": access_token,
        "token_type": "bearer"
    }

# Recap: Retrieves the profile of the currently logged-in user.
@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# Recap: Retrieves a list of all users for admin review.
@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_admin)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users
