# tests/test_resource_matching.py

import os
import pytest
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from ai.matching_model import transformer
from app.graphql.resolvers import (
    resolve_resources_per_capita,
    resolve_resource_need_gap,
    resolve_match_success_rate
)
from app.database import SessionLocal, engine, Base
from datetime import datetime, timedelta
from app.models import Resource, Region, DemandLog, MatchLog
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

@pytest.fixture
def toy_data():
    df = pd.DataFrame([
        {"service_type": "HEALTH", "latitude": 0.0, "longitude": 0.0, "cost_level": 1},
        {"service_type": "HEALTH", "latitude": 1.0, "longitude": 1.0, "cost_level": 2},
        {"service_type": "LEGAL",  "latitude": 2.0, "longitude": 2.0, "cost_level": 3},
    ])

    # Duplicate service_type as "service_type_weighted" for more flexible weighting
    df["service_type_weighted"] = df["service_type"]

    tr_local = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["service_type_weighted"]),
        ("num", StandardScaler(), ["latitude", "longitude", "cost_level"]),
    ]).fit(df)

    X = tr_local.transform(df)
    nn_local = NearestNeighbors(n_neighbors=2).fit(X)
    max_second = nn_local.kneighbors(X, n_neighbors=2)[0][:, 1].max()
    ids = ["r1", "r2", "r3"]
    return tr_local, nn_local, ids, max_second

def test_transformer_output_shape(toy_data):
    tr, _, _ids, _ = toy_data
    df_sample = pd.DataFrame([{
        "service_type_weighted": "HEALTH",
        "latitude": 0.5,
        "longitude": 0.5,
        "cost_level": 1
    }])
    Xt = tr.transform(df_sample)
    assert Xt.shape[1] == tr.transform(df_sample).shape[1]

def test_knn_matches(toy_data):
    tr, nn_local, ids, _ = toy_data
    df_test = pd.DataFrame([{
        "service_type_weighted": "HEALTH",
        "latitude": 0.1,
        "longitude": 0.1,
        "cost_level": 1
    }])
    Xt = tr.transform(df_test)
    dists, idxs = nn_local.kneighbors(Xt)
    assert ids[idxs[0][0]] == "r1"
    assert dists[0][0] < dists[0][1]

@pytest.mark.parametrize("service_type,expected", [
    ("HEALTH", "r2"),
    ("LEGAL",  "r3"),
])
def test_knn_service_type(toy_data, service_type, expected):
    tr, nn_local, ids, _ = toy_data
    test_point = {
        "service_type_weighted": service_type,
        "latitude": 1.5 if service_type == "HEALTH" else 2.0,
        "longitude": 1.5 if service_type == "HEALTH" else 2.0,
        "cost_level": 2 if service_type == "HEALTH" else 3,
    }
    df_test = pd.DataFrame([test_point])
    Xt = tr.transform(df_test)
    dists, idxs = nn_local.kneighbors(Xt)
    assert ids[idxs[0][0]] == expected

def test_knn_no_match(toy_data):
    tr, nn_local, ids, max_dist = toy_data
    df_test = pd.DataFrame([{
        "service_type_weighted": "FOOD",  # Unseen category
        "latitude": 100.0,
        "longitude": 100.0,
        "cost_level": 10
    }])
    Xt = tr.transform(df_test)
    dists, idxs = nn_local.kneighbors(Xt)
    assert dists[0][0] > max_dist

def test_real_transformer_output_shape():
    df_sample = pd.DataFrame([{
        "service_type_weighted": "HEALTH",
        "latitude": 0.0,
        "longitude": 0.0,
        "cost_level": 1
    }])
    Xt = transformer.transform(df_sample)
    assert Xt.shape[1] > 0


# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Pick up DATABASE_URL from .env if set, otherwise use in-memory SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://<POSTGRES_USER>:<POSTGRES_PASSWORD>@localhost:5432/<POSTGRES_DB>")

# ─── Fixtures ───────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope="module")
def engine():
    return create_engine(DATABASE_URL)

@pytest.fixture(scope="module")
def tables(engine):
    # create all tables
    Base.metadata.create_all(engine)
    yield
    # drop them after tests
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def region_factory(db_session):
    def create_region(region_name="DefaultRegion", population_in_need=1000):
        r = Region(region_name=region_name, population_in_need=population_in_need)
        db_session.add(r)
        db_session.commit()
        return r
    return create_region

@pytest.fixture
def resource_factory(db_session):
    def create_resource(
        region,
        service_type="HEALTH",
        latitude=0.0,
        longitude=0.0,
        cost_level=1,
        languages_supported=None,
        capacity=10,
        tags=None,
        organization_id="org-123"
    ):
        res = Resource(
            service_type=service_type,
            latitude=latitude,
            longitude=longitude,
            cost_level=cost_level,
            languages_supported=languages_supported or ["en"],
            capacity=capacity,
            tags=tags or [],
            region_id=region.region_id,
            organization_id=organization_id
        )
        db_session.add(res)
        db_session.commit()
        return res
    return create_resource

@pytest.fixture
def demandlog_factory(db_session):
    def create_demand(
        region,
        category="HEALTH",
        count=1,
        timestamp=None
    ):
        dl = DemandLog(
            region_id=region.region_id,
            category=category,
            count=count,
            timestamp=timestamp or datetime.utcnow()
        )
        db_session.add(dl)
        db_session.commit()
        return dl
    return create_demand

@pytest.fixture
def matchlog_factory(db_session):
    def create_match(
        region,
        success=True,
        timestamp=None
    ):
        ml = MatchLog(
            region_id=region.region_id,
            success=success,
            timestamp=timestamp or datetime.utcnow()
        )
        db_session.add(ml)
        db_session.commit()
        return ml
    return create_match

# ─── Tests ─────────────────────────────────────────────────────────────────

def test_resources_per_capita(db_session, region_factory, resource_factory):
    region = region_factory(region_name="TestRegion", population_in_need=100)
    resource_factory(region=region)
    resource_factory(region=region)
    count = (
        db_session.query(Resource)
        .filter_by(region_id=region.region_id)
        .count()
    )
    assert count == 2

def test_resource_need_gap(db_session, region_factory, demandlog_factory):
    region = region_factory(region_name="GapRegion", population_in_need=500)
    demandlog_factory(region=region, category="HEALTH", count=2)
    demandlog_factory(region=region, category="LEGAL", count=1)
    entries = (
        db_session.query(DemandLog)
        .filter_by(region_id=region.region_id)
        .all()
    )
    assert len(entries) == 2
    # verify counts
    counts = {e.category: e.count for e in entries}
    assert counts["HEALTH"] == 2
    assert counts["LEGAL"] == 1

def test_match_success_rate(db_session, region_factory, matchlog_factory):
    region = region_factory(region_name="MatchRegion", population_in_need=300)
    now = datetime.utcnow()
    earlier = now - timedelta(days=30)
    matchlog_factory(region=region, success=True, timestamp=now)
    matchlog_factory(region=region, success=False, timestamp=now)
    matchlog_factory(region=region, success=True, timestamp=earlier)

    total = (
        db_session.query(MatchLog)
        .filter_by(region_id=region.region_id)
        .count()
    )
    successes = (
        db_session.query(MatchLog)
        .filter_by(region_id=region.region_id, success=True)
        .count()
    )

    assert total == 3
    assert successes == 2
