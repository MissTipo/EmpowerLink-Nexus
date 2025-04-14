# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    role: Optional[str] = "Organization"  # Default role

class OrganizationCreate(OrganizationBase):
    password: str  # Plain text password to be hashed

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# For authentication responses
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    org_id: Optional[int] = None

