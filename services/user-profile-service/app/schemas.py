# user-profile-service/app/schemas.py
from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     orm_mode = True

