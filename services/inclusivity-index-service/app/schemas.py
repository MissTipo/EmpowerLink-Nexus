from pydantic import BaseModel
from datetime import datetime

class MetricIn(BaseModel):
    region_id: int
    category:  str
    value:     float

class MetricOut(MetricIn):
    id:        int
    timestamp: datetime

class IndexOut(BaseModel):
    value: float
    # region_id: int
    # index:     float

