from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Activity schemas
class ActivityBase(BaseModel):
    name: str
    description: str
    schedule: str
    max_participants: int

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    created_at: datetime
    updated_at: datetime
    participants: List[User] = []

    class Config:
        from_attributes = True

# Participant schemas
class ParticipantBase(BaseModel):
    activity_id: int
    user_id: int

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase):
    id: int
    registered_at: datetime
    activity: Optional[Activity] = None
    user: Optional[User] = None

    class Config:
        from_attributes = True