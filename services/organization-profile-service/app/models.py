# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)           # Organization name
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    location = Column(String, nullable=True)
    role = Column(String, nullable=False, default="Organization")  # e.g., Organization, Policy Maker, Admin
    password = Column(String, nullable=False)         # Hashed password
    created_at = Column(DateTime(timezone=True), server_default=func.now())

