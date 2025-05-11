from ariadne import QueryType
from app.database import SessionLocal
from app.models import InclusivityMetric
from workers.tasks import compute_inclusivity_index

query = QueryType()

@query.field("getMetrics")
def resolve_get_metrics(_, info, regionId):
    db = SessionLocal()
    try:
        rows = db.query(InclusivityMetric).filter_by(region_id=regionId).all()
    finally:
        db.close()
    return [
        {
            "id":        m.id,
            "regionId":  m.region_id,
            "category":  m.category,
            "value":     m.value,
            "timestamp": m.timestamp.isoformat(),
        }
        for m in rows
    ]
@query.field("computeInclusivityIndex")
def resolve_compute_index(_, info, regionId):
    from workers.tasks import compute_inclusivity_index
    async_result = compute_inclusivity_index.delay(regionId)
    return {"value": async_result.get(timeout=36000)}
