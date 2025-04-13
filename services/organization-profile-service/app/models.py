from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # Stored as a hashed value ideally
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

