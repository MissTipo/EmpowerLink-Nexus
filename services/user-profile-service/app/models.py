# app/models.py

from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, index=True)
    gender = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
