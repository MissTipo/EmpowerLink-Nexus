import os

# Use SQLite in-memory database for testing
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db


# Create the test engine and session
TEST_DATABASE_URL = os.environ["DATABASE_URL"]  
engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a test fixture that sets up the database
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Override the get_db dependency for testing
@pytest.fixture()
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a TestClient fixture that uses the overridden dependency
@pytest.fixture()
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

# -------------------------------
# REST Endpoint Tests
# -------------------------------

def test_create_user_profile_rest(client):
    # Test the REST endpoint at /api/users/ for creating a user profile
    payload = {
        "phone_number": "0700000001",
        "name": "Alice",
        "gender": "Female",
        "age": 25,
        "location": "Nairobi"
    }
    response = client.post("/api/users/", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["name"] == "Alice"
    assert data["phone_number"] == "0700000001"


def test_get_user_profile_rest(client):
    # First, create a user profile via REST
    payload = {
        "phone_number": "0700000002",
        "name": "Bob",
        "gender": "Male",
        "age": 30,
        "location": "Mombasa"
    }
    create_resp = client.post("/api/users/", json=payload)
    user_id = create_resp.json()["id"]

    # Retrieve the created user profile
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Bob"


def test_update_user_profile_rest(client):
    # First, create a user profile via REST
    payload = {
        "phone_number": "0700000003",
        "name": "Charlie",
        "gender": "Male",
        "age": 28,
        "location": "Kisumu"
    }
    create_resp = client.post("/api/users/", json=payload)
    user_id = create_resp.json()["id"]

    # Update the user's location
    update_payload = {
        "name": "Charlie",
        "gender": "Male",
        "age": 28,
        "location": "Eldoret"
    }
    response = client.put(f"/api/users/{user_id}", json=update_payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["location"] == "Eldoret"

# -------------------------------
# GraphQL Tests
# -------------------------------

def execute_graphql_query(client, query: str, variables: dict = None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = client.post("/graphql", json=payload)
    assert response.status_code == 200, f"Status: {response.status_code}, {response.text}"
    return response.json()["data"]

def test_create_and_get_user_profile_graphql(client):
    # Test GraphQL mutation to create a user profile
    create_mutation = """
    mutation CreateUserProfile($input: UserProfileInput!) {
      createUserProfile(input: $input) {
        id
        name
        phone_number
        location
      }
    }
    """
    variables = {
        "input": {
            "phone_number": "0700000004",
            "name": "Diana",
            "gender": "Female",
            "age": 22,
            "location": "Nakuru"
        }
    }
    create_data = execute_graphql_query(client, create_mutation, variables)
    created_user = create_data["createUserProfile"]
    assert created_user["name"] == "Diana"
    user_id = created_user["id"]

    # Now test GraphQL query to retrieve the created profile
    query = """
    query GetUserProfile($id: ID!) {
      getUserProfile(id: $id) {
        id
        name
        phone_number
        location
      }
    }
    """
    query_data = execute_graphql_query(client, query, {"id": user_id})
    retrieved_user = query_data["getUserProfile"]
    assert retrieved_user["name"] == "Diana"
    assert retrieved_user["phone_number"] == "0700000004"

def test_update_user_profile_graphql(client):
    # First, create a user via GraphQL
    create_mutation = """
    mutation CreateUserProfile($input: UserProfileInput!) {
      createUserProfile(input: $input) {
        id
        name
        location
      }
    }
    """
    variables = {
        "input": {
            "phone_number": "0700000005",
            "name": "Eve",
            "gender": "Female",
            "age": 35,
            "location": "Thika"
        }
    }
    create_data = execute_graphql_query(client, create_mutation, variables)
    user_id = create_data["createUserProfile"]["id"]

    # Update the user's name via GraphQL
    update_mutation = """
    mutation UpdateUserProfile($id: ID!, $input: UserProfileInput!) {
      updateUserProfile(id: $id, input: $input) {
        id
        name
        location
      }
    }
    """
    update_variables = {
        "id": user_id,
        "input": {
            "phone_number": "0700000005",
            "name": "Evelyn",
            "gender": "Female",
            "age": 35,
            "location": "Machakos"
        }
    }
    update_data = execute_graphql_query(client, update_mutation, update_variables)
    updated_user = update_data["updateUserProfile"]
    assert updated_user["name"] == "Evelyn"
    assert updated_user["location"] == "Machakos"

