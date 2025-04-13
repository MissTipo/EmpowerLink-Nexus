# app/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str
    email: str
    role: str

class OrganizationCreate(OrganizationBase):
    password: str

class OrganizationLogin(BaseModel):
    email: str
    password: str

class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AuthPayload(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenInfo(BaseModel):
    email: Optional[str]

