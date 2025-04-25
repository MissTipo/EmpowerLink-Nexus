# tests/test_inclusivity_index.py

import os
import pytest
from app import models

# 1) Override DATABASE_URL before importing any app modules
os.environ["DATABASE_URL"] = "sqlite:///./test_inclusivity.db"

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 2) Create engine & sessionmaker with check_same_thread=False
TEST_DB_URL = os.environ["DATABASE_URL"]
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 3) Monkey‐patch the app's database module
import app.database as database_mod
database_mod.engine = engine
database_mod.SessionLocal = SessionLocal

# 4) Import Base and create/drop tables once per session
from app.database import Base
Base.metadata.create_all(bind=engine)
@pytest.fixture(scope="session", autouse=True)
def teardown_database():
    yield
    Base.metadata.drop_all(bind=engine)
    # clean up the sqlite file
    try:
        os.remove("test_inclusivity.db")
    except OSError:
        pass

# 5) Now import the FastAPI app and testing utilities
from app.main import app
from fastapi.testclient import TestClient
from workers.tasks import compute_inclusivity_index

client = TestClient(app)

@pytest.fixture
def db():
    """Provide a fresh session per test."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_and_get_metrics_rest(db):
    # POST /api/metrics/
    payload = {"category": "healthcare", "value": 0.8, "region_id": 1}
    resp = client.post("/api/metrics/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] == "healthcare"
    assert data["value"] == 0.8
    assert data["region_id"] == 1

    # GET /api/metrics/1
    resp2 = client.get("/api/metrics/1")
    assert resp2.status_code == 200
    items = resp2.json()
    assert isinstance(items, list)
    assert items[0]["category"] == "healthcare"

def test_compute_inclusivity_index_task(db):
    # Seed metrics across all categories for region 2
    metrics = [
        models.InclusivityMetric(region_id=2, category="healthcare",     value=0.5),
        models.InclusivityMetric(region_id=2, category="education",      value=1.0),
        models.InclusivityMetric(region_id=2, category="legal_access",   value=0.0),
        models.InclusivityMetric(region_id=2, category="gender_equality", value=0.5),
    ]
    db.add_all(metrics)
    db.commit()

    # With equal weights (0.25 each): (0.5 + 1.0 + 0.0 + 0.5)/4 = 0.5
    idx = compute_inclusivity_index(2)
    assert isinstance(idx, float)
    assert idx == pytest.approx(0.5, rel=1e-3)

def test_get_inclusivity_index_rest(monkeypatch):
    # Monkeypatch Celery .delay to return a dummy result
    class Dummy:
        def __init__(self, v): self._v = v
        def get(self, timeout=None): return self._v

    monkeypatch.setattr(
        "workers.tasks.compute_inclusivity_index.delay",
        lambda region: Dummy(0.77)
    )

    resp = client.get("/api/inclusivity-index/42")
    assert resp.status_code == 200
    assert resp.json() == {"value": 0.77}

def test_graphql_get_metrics_and_index(db, monkeypatch):
    # Seed one metric for region 3
    metric = models.InclusivityMetric(region_id=3, category="healthcare", value=0.9)
    db.add(metric)
    db.commit()

    # 1) GraphQL getMetrics
    query1 = """
    query {
      getMetrics(regionId: 3) {
        id
        category
        value
        regionId
      }
    }
    """
    resp1 = client.post("/graphql", json={"query": query1})
    assert resp1.status_code == 200
    got = resp1.json()["data"]["getMetrics"]
    assert len(got) == 1
    assert got[0]["value"] == 0.9

    # 2) GraphQL computeInclusivityIndex
    class Dummy:
        def __init__(self, v): self._v = v
        def get(self, timeout=None): return self._v

    monkeypatch.setattr(
        "workers.tasks.compute_inclusivity_index.delay",
        lambda region: Dummy(0.42)
    )
    query2 = """
    query {
      computeInclusivityIndex(regionId: 3) {
        value
      }
    }
    """
    resp2 = client.post("/graphql", json={"query": query2})
    assert resp2.status_code == 200
    val = resp2.json()["data"]["computeInclusivityIndex"]["value"]
    assert val == 0.42

