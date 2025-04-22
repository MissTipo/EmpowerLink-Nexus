# ai/data_loader.py

from app.database import SessionLocal
from app.models import Resource

def load_data():
    db = SessionLocal()
    resources = db.query(Resource).all()
    db.close()

    texts = []
    labels = []

    for r in resources:
        # Convert structured fields into a text string for vectorization
        tags_str = " ".join(r.tags) if isinstance(r.tags, list) else ""
        langs_str = " ".join(r.languages_supported) if isinstance(r.languages_supported, list) else ""
        features = f"{r.service_type} cost:{r.cost_level} capacity:{r.capacity} {tags_str} {langs_str}"
        texts.append(features)

        # Label could be service_type or another field depending on your use case
        labels.append(r.service_type)

    return texts, labels

