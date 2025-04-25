from celery import Celery
from config.settings import settings
from app.database import SessionLocal
from app.models import InclusivityMetric
from sqlalchemy.sql import func

celery = Celery(__name__, broker=settings.broker_url, backend=settings.result_backend)

@celery.task
def compute_inclusivity_index(region_id):
    db = SessionLocal()
    metrics = db.query(InclusivityMetric).filter(InclusivityMetric.region_id == region_id).all()

    categories = ['healthcare', 'education', 'legal_access', 'gender_equality']
    weights = {
        'healthcare': settings.healthcare_weight,
        'education': settings.education_weight,
        'legal_access': settings.legal_access_weight,
        'gender_equality': settings.gender_equality_weight
    }

    index = 0.0
    for category in categories:
        values = [m.value for m in metrics if m.category == category]
        avg = sum(values) / len(values) if values else 0.0
        index += avg * weights[category]

    db.close()
    return round(index, 2)

