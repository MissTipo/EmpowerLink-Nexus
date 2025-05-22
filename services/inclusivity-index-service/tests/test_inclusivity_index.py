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

from celery.result import AsyncResult

@pytest.fixture(scope="session")
def client():
    """
    Provides a TestClient instance pointed at your FastAPI/Ariadne app.
    """
    return TestClient(app)

def test_create_and_get_metrics_rest(db, client):
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

def test_compute_inclusivity_index_task(db, client):
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

def test_get_inclusivity_index_rest(monkeypatch, client):
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

def test_graphql_get_metrics_and_index(db, monkeypatch, client):
    # Seed one metric for region 3
    metric = models.InclusivityMetric(region_id=3, category="healthcare", value=0.9)
    db.add(metric)
    db.commit()

    # 1) getMetrics
    resp1 = client.post("/graphql", json={
        "query": """
        query {
          getMetrics(regionId: 3) {
            value
          }
        }
        """
    })
    assert resp1.status_code == 200
    assert resp1.json()["data"]["getMetrics"][0]["value"] == 0.9

    # 2) computeInclusivityIndex → returns TaskHandle
    class DummyHandle:
        def __init__(self, tid):
            self.id = tid
            self.status = "PENDING"

    monkeypatch.setattr(
        "workers.tasks.compute_inclusivity_index.delay",
        lambda region: DummyHandle("task-123")
    )

    resp2 = client.post("/graphql", json={
        "query": """
        query {
          computeInclusivityIndex(regionId: 3) {
            taskId
            status
          }
        }
        """
    })
    assert resp2.status_code == 200
    data2 = resp2.json()["data"]["computeInclusivityIndex"]
    assert data2["taskId"] == "task-123"
    assert data2["status"] == "PENDING"

    # 3) getTaskStatus → simulate a completed Celery result
    monkeypatch.setattr(AsyncResult, "ready", lambda self: True)
    monkeypatch.setattr(AsyncResult, "status", "SUCCESS", raising=False)
    monkeypatch.setattr(AsyncResult, "result", 0.42, raising=False)

    resp3 = client.post("/graphql", json={
        "query": """
        query {
          getTaskStatus(taskId: "task-123") {
            status
            value
            error
          }
        }
        """
    })
    assert resp3.status_code == 200
    data3 = resp3.json()["data"]["getTaskStatus"]
    assert data3["status"] == "SUCCESS"
    assert data3["value"] == 0.42
    assert data3["error"] is None
