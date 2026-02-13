from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import os
from app import models
from app.database import get_db

# Password hashing setup
# Argon2 is a secure algorithm for hashing passwords
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Helper function to check if a password matches its hash
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Helper function to create a secure hash of a password
def get_password_hash(password):
    return pwd_context.hash(password)

# Secret key used to sign the tokens (should be kept safe!)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# Security scheme to handle Bearer tokens
security = HTTPBearer()

# Function to create a new login token (JWT)
def create_access_token(data: dict):
    to_encode = data.copy()
    # We create a token that stays valid (no expiration for simplicity)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to get the current user based on the provided token
def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = auth.credentials # Get the token from the request
    
    # Error to show if login fails
    error_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Login required or session expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token to find the user's email
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise error_response
    except jwt.JWTError:
        # If token is invalid or broken
        raise error_response
    
    # Find the user in the database
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise error_response
        
    return user

# Function to check if the current user is an Admin
def get_current_admin(current_user: models.User = Depends(get_current_user)):
    # Check if the user's role is 'admin'
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )
    return current_user
