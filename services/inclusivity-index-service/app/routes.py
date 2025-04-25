from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import InclusivityMetric
from app.schemas import MetricIn, MetricOut, IndexOut
from workers.tasks import compute_inclusivity_index

router = APIRouter(prefix="/api", tags=["inclusivity"])

@router.post("/metrics/", response_model=MetricOut)
def create_metric(payload: MetricIn, db: Session = Depends(get_db)):
    db_metric = InclusivityMetric(**payload.model_dump())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.get("/metrics/{region_id}", response_model=list[MetricOut])
def list_metrics(region_id: int, db: Session = Depends(get_db)):
    return db.query(InclusivityMetric).filter_by(region_id=region_id).all()

@router.get("/inclusivity-index/{region_id}", response_model=IndexOut)
def get_index(region_id: int):
    # fire-and-forget + wait
    task = compute_inclusivity_index.delay(region_id)
    try:
        idx = task.get(timeout=10)
    except Exception as e:
        raise HTTPException(500, f"Index computation failed: {e}")
    return {"value": idx}

