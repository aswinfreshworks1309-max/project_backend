from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    full_name: Optional[str] = None
    role: Optional[str] = "user"
    

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True  
