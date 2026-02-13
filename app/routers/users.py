from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import auth

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

# 1. Sign Up Endpoint: Creates a new user in the database
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # First, hash the password so it isn't stored in plain text
    hashed_password = auth.get_password_hash(user.password)
    
    # Create a new user object
    db_user = models.User(
        name=user.name, 
        email=user.email, 
        hashed_password=hashed_password, 
        full_name=user.full_name,
        role=user.role
    )
    
    # Save the user to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # Get the new ID from the database
    return db_user

# 2. Login Endpoint: Checks credentials and returns a secure token
@router.post("/login")
def login(user_credentials: schemas.UserCreate, db: Session = Depends(get_db)):
    # Look for the user by their email
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    # Check if user exists and if password is correct
    if not user or not auth.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Create a JWT token containing the user's email
    access_token = auth.create_access_token(data={"sub": user.email})
    
    # Send back the user info and the token to the frontend
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "access_token": access_token,
        "token_type": "bearer"
    }

# 3. Profile Endpoint: Returns info about the logged-in user
@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    # 'auth.get_current_user' automatically checks the token and finds the user
    return current_user

# 4. List Users Endpoint (Admin Only): Shows all users registered
@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_admin)):
    # 'auth.get_current_admin' ensures only admins can see this list
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users
