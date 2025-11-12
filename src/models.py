"""
Pydantic models for API request/response handling
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    profile_picture_url: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ActivityBase(BaseModel):
    name: str
    description: str
    schedule: str
    max_participants: int

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    description: Optional[str] = None
    schedule: Optional[str] = None
    max_participants: Optional[int] = None

class Activity(ActivityBase):
    id: int
    created_at: datetime
    updated_at: datetime
    participants: List[User] = []
    
    class Config:
        from_attributes = True

class ActivityResponse(BaseModel):
    """Response format that matches the original API structure"""
    description: str
    schedule: str
    max_participants: int
    participants: List[str]  # List of email addresses

class SignupRequest(BaseModel):
    email: str

class SignupResponse(BaseModel):
    message: str

class UnregisterRequest(BaseModel):
    email: str

class UnregisterResponse(BaseModel):
    message: str