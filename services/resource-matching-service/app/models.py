# app/models.py
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.types import JSON
from app.database import Base

class Resource(Base):
    __tablename__ = "resources"

    resource_id = Column(
      UUID(as_uuid=True),
      primary_key=True,
      default=uuid.uuid4,      # <— auto‐generate
      nullable=False,
      unique=True
    )
    service_type = Column(String, nullable=False)
    latitude     = Column(Float, nullable=False)
    longitude    = Column(Float, nullable=False)
    cost_level   = Column(Integer, nullable=False)
    languages_supported = Column(JSON, nullable=False)
    capacity     = Column(Integer, nullable=False)
    tags         = Column(JSON, nullable=False)

