# tests/test_resource_matching.py

import pytest
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from ai.matching_model import transformer

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
