# app/models.py
import uuid
import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, ForeignKey, Index, Enum, func
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
    region_id = Column(Integer, ForeignKey("regions.region_id"), nullable=False)
    organization_id = Column(String, nullable=False)


# Analytics tables

# 1. Region
class Region(Base):
    __tablename__ = "regions"

    region_id        = Column(Integer, primary_key=True)
    region_name      = Column(String, nullable=False, unique=True)
    population_in_need = Column(Integer, nullable=False)

    # optional backref:
    # resources = relationship("Resource", back_populates="region")

# 3. DemandLog
class DemandLog(Base):
    __tablename__ = "demand_logs"

    demand_id         = Column(Integer, primary_key=True, autoincrement=True)
    region_id  = Column(Integer, ForeignKey("regions.region_id"), nullable=False)
    category   = Column(String, nullable=False)
    count      = Column(Integer, default=0)
    timestamp  = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_demand_region_category", "region_id", "category"),
    )


# 4. MatchLog
class MatchLog(Base):
    __tablename__ = "match_logs"

    match_id         = Column(Integer, primary_key=True, autoincrement=True)
    region_id  = Column(Integer, ForeignKey("regions.region_id"), nullable=False)
    success    = Column(Boolean, nullable=False)
    timestamp  = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_match_region_month", "region_id", func.date_trunc('month', timestamp)),
    )

