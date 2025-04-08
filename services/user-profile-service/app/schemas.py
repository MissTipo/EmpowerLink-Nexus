# user-profile-service/app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserProfileBase(BaseModel):
    phone_number: str
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    location: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    location: Optional[str] = None

class UserProfileResponse(UserProfileBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

