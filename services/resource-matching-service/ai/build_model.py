import os
import pickle
import pandas as pd
import argparse

from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app.models import Resource

from sklearn.neighbors import NearestNeighbors
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from faker import Faker

# ─── Helpers ────────────────────────────────────────────────────────────────────

def ensure_tables():
    """Create tables in DB if they don't exist yet."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ensured.")

def seed_sample_resources(n=5):
    """Insert n fake Resource rows if table is empty."""
    db: Session = SessionLocal()
    count = db.query(Resource).count()
    if count > 0:
        print(f"🚧 Skipping seeding: table already has {count} rows.")
        db.close()
        return

    fake = Faker()
    samples = []
    for _ in range(n):
        samples.append(
            Resource(
                service_type=fake.random_element(elements=("health","legal","social")),
                latitude=float(fake.latitude()),
                longitude=float(fake.longitude()),
                cost_level=fake.random_int(min=1, max=5),
                languages_supported=fake.random_elements(elements=("en","sw","fr","es"), length=2, unique=True),
                capacity=fake.random_int(min=1, max=100),
                tags=fake.random_elements(elements=("free","childcare","accessible","remote"), length=2)
            )
        )
    db.add_all(samples)
    db.commit()
    print(f"🌱 Seeded {n} sample resources.")
    db.close()

def fetch_resources_from_db() -> pd.DataFrame:
    """Load all Resource rows into a DataFrame."""
    db: Session = SessionLocal()
    resources = db.query(Resource).all()
    db.close()
    data = []
    for r in resources:
        data.append({
            "id": str(r.resource_id),
            "service_type": r.service_type,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "cost_level": r.cost_level,
        })
    return pd.DataFrame(data)

def build_transformer():
    return ColumnTransformer([
        ("cat", OneHotEncoder(), ["service_type"]),
        ("num", StandardScaler(), ["latitude", "longitude", "cost_level"]),
    ])

def save_artifacts(transformer, knn, resource_ids):
    os.makedirs("ai", exist_ok=True)
    with open("ai/transformer.pkl", "wb") as f:
        pickle.dump(transformer, f)
    with open("ai/knn_model.pkl", "wb") as f:
        pickle.dump(knn, f)
    with open("ai/resource_ids.pkl", "wb") as f:
        pickle.dump(resource_ids, f)
    print("✅ Artifacts saved to ai/")

# ─── Main pipeline ─────────────────────────────────────────────────────────────

def build_and_save_model(seed: bool):
    ensure_tables()
    if seed:
        seed_sample_resources()

    df = fetch_resources_from_db()
    if df.empty:
        print("❌ No resources found in database. Use --seed to insert sample data.")
        return

    transformer = build_transformer()
    X = transformer.fit_transform(df)

    knn = NearestNeighbors(n_neighbors=5, metric="euclidean")
    knn.fit(X)

    save_artifacts(transformer, knn, list(df["id"]))
    print(f"✅ KNN model trained on {len(df)} resources.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build & save KNN model artifacts")
    parser.add_argument(
        "--seed", action="store_true",
        help="If set, seed the resources table with sample data before training."
    )
    args = parser.parse_args()
    build_and_save_model(seed=args.seed)

