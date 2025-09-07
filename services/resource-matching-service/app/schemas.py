from pydantic import BaseModel
from typing import List, Optional

class GeoPoint(BaseModel):
    latitude: float
    longitude: float

class MatchRequest(BaseModel):
    user_id: str
    service_type: str
    location: GeoPoint
    age: Optional[int]
    gender: Optional[str]
    languages: Optional[List[str]]
    cost_level: Optional[int]
    max_distance_km: Optional[float]
    limit: int = 5

class ResourceOut(BaseModel):
    resource_id: str
    service_type: str
    latitude: float
    longitude: float
    cost_level: int
    languages_supported: List[str]
    capacity: int
    tags: List[str]

    class Config:
        from_attributes = True

class ResourceMatch(BaseModel):
    resource: ResourceOut
    score: float
