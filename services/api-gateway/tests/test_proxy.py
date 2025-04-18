import pytest
import respx
from fastapi.testclient import TestClient
from src.app import app, SERVICE_MAP

client = TestClient(app)

# A small helper to build a minimal GraphQL payload
def gql(query: str, variables: dict = None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    return payload

@respx.mock
def test_get_user_profile_proxied():
    # Arrange: mock the downstream user-profile-service endpoint
    url = SERVICE_MAP["getUserProfile"]
    # Simulate that service returning a user
    respx.post(url).respond(
        json={"data": {"getUserProfile": {"id": "1", "name": "Alice"}}}
    )

    # Act: call our gateway
    query = """
      query GetUserProfile {
        getUserProfile(id: "1") {
          id
          name
        }
      }
    """
    resp = client.post("/graphql", json=gql(query))

    # Assert
    assert resp.status_code == 200
    data = resp.json()["data"]["getUserProfile"]
    assert data["id"] == "1"
    assert data["name"] == "Alice"

@respx.mock
def test_unknown_operation_returns_error():
    # Arrange: no mock for this operation name
    query = """
      mutation UnknownOp {
        doSomething { result }
      }
    """
    # Act
    resp = client.post("/graphql", json=gql(query))

    # Assert
    assert resp.status_code == 400
    errors = resp.json()["errors"]
    assert any("Unknown operation" in e["message"] for e in errors)

