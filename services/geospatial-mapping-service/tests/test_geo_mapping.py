# tests/test_geo_mapping.py

import os
# Disable Ryuk’s background reaper thread
os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"

import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def client():
    """
    1) Spin up one PostGIS container
    2) Enable the PostGIS extension
    3) Monkey-patch DATABASE_URL
    4) Rebind app.database.engine & SessionLocal
    5) Create all tables
    6) Yield a TestClient(app)
    7) Teardown: Drop tables, stop container
    """
    # 1) start container
    pg = PostgresContainer("postgis/postgis:15-3.4")
    pg.start()
    url = pg.get_connection_url()

    # 2) enable PostGIS
    engine = create_engine(url)
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))

    # 3) set env for your app code
    os.environ["DATABASE_URL"] = url

    # 4) rebind in app.database
    import app.database as db_mod
    db_mod.engine = engine
    db_mod.SessionLocal = sessionmaker(
        autoflush=False, autocommit=False, bind=engine
    )

    # 5) create tables
    from app.database import Base
    Base.metadata.create_all(bind=engine)

    # 6) import & yield client
    from app.main import app
    client = TestClient(app)
    yield client

    # teardown
    db_mod.SessionLocal.close_all()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    pg.stop()


def test_list_resources_empty(client):
    resp = client.get("/map/resources")
    assert resp.status_code == 200
    data = resp.json()
    assert data["type"] == "FeatureCollection"
    assert data["features"] == []

def test_create_and_list_resource(client):
    from app.models import ResourceLocation
    from app.database import SessionLocal
    from geoalchemy2.elements import WKTElement

    db = SessionLocal()
    loc = ResourceLocation(
        resource_id="r1",
        service_type="HEALTH",
        location=WKTElement("POINT(36.81667 -1.28333)", srid=4326),
    )
    db.add(loc)
    db.commit()
    db.close()

    resp = client.get("/map/resources")
    assert resp.status_code == 200
    features = resp.json()["features"]
    assert len(features) == 1
    feat = features[0]
    assert feat["properties"]["resource_id"] == "r1"
    assert feat["properties"]["service_type"] == "HEALTH"
    assert feat["geometry"]["type"] == "Point"

def test_service_deserts_no_deserts(client):
    resp = client.get("/map/service-deserts?radius_km=10000")
    assert resp.status_code == 200
    data = resp.json()
    assert data["type"] == "FeatureCollection"
    assert data["features"] == []

def test_graphql_all_locations(client):
    query = """
    query {
      allResourceLocations
    }
    """
    resp = client.post("/graphql", json={"query": query})
    assert resp.status_code == 200
    fc = resp.json()["data"]["allResourceLocations"]
    assert fc["type"] == "FeatureCollection"
    assert isinstance(fc["features"], list)


def test_graphql_service_deserts(client):
    # ensure no resources remain
    from app.database import SessionLocal
    from app.models import ResourceLocation
    db = SessionLocal()
    db.query(ResourceLocation).delete()
    db.commit()
    db.close()

    query = """
    query($r: Float!) {
      serviceDeserts(radiusKm: $r)
    }
    """
    # use a very large radius so the resolver short-circuits immediately
    resp = client.post("/graphql", json={
        "query": query,
        "variables": {"r": 1.0}
    })
    assert resp.status_code == 200
    fc = resp.json()["data"]["serviceDeserts"]
    assert fc["type"] == "FeatureCollection"
    assert isinstance(fc["features"], list)

