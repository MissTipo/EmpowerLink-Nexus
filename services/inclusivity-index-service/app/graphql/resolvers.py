from ariadne import QueryType
from app.database import SessionLocal
from app.models import InclusivityMetric
from workers.tasks import compute_inclusivity_index
from celery.result import AsyncResult

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
    async_result = compute_inclusivity_index.delay(regionId)
    # return {"value": async_result.get(timeout=36000)}
    return {"taskId": async_result.id, "status": async_result.status}

@query.field("getTaskStatus")
def resolve_task_status(_, info, taskId):
    r = AsyncResult(taskId)
    if r.ready():
        # SUCCESS or FAILURE
        return {
            "status": r.status,
            "value": r.result if r.status == "SUCCESS" else None,
            "error": str(r.result) if r.status == "FAILURE" else None,
        }
    # still pending
    return {"status": r.status, "value": None, "error": None}

@query.field("getInclusivityTrend")
def resolve_get_inclusivity_trend(*_, regionId):
    db = SessionLocal()
    metrics = (
        db.query(InclusivityMetric)
        .filter(InclusivityMetric.region_id == regionId)
        .order_by(InclusivityMetric.timestamp.asc())
        .all()
    )
    return [
        {
            "id": m.id,
            "value": m.value,
            "timestamp": m.timestamp.isoformat()
        }
        for m in metrics
    ]
