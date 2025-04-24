from sqlalchemy import Column, String, Integer
from geoalchemy2 import Geometry
from app.database import Base

class ResourceLocation(Base):
    __tablename__ = "resource_locations"

    id           = Column(Integer, primary_key=True, index=True)
    resource_id  = Column(String, unique=True, nullable=False, index=True)
    service_type = Column(String, nullable=False, index=True)
    location     = Column(Geometry("POINT", srid=4326), nullable=False)

