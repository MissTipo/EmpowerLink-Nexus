# user-profile-service/app/models.py
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)  # Optional if using phone-based identifier
    gender = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    phone_number = Column(String, unique=True, index=True)  # Could be the identifier
    created_at = Column(DateTime(timezone=True), server_default=func.now())

