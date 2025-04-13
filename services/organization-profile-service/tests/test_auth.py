# tests/test_auth.py

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set the test database URL BEFORE importing anything that uses it.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.main import app
from app.database import Base, get_db

# Create a test engine and session for an in-memory SQLite DB.
TEST_DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(os.environ["DATABASE_URL"], connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture: Set up and tear down the database schema.
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Fixture: Provide a test database session.
@pytest.fixture()
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fixture: Provide a TestClient that overrides the get_db dependency.
@pytest.fixture()
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# Helper function to execute GraphQL queries/mutations.
def execute_graphql_query(client, query: str, variables: dict = None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = client.post("/graphql", json=payload)
    assert response.status_code == 200, f"Status: {response.status_code}, {response.text}"
    data = response.json().get("data")
    assert data is not None, f"GraphQL error: {response.json().get('errors')}"
    return data

# ----------------------------
# GraphQL Tests
# ----------------------------

def test_register_and_login_graphql(client):
    # Test registration
    register_mutation = """
    mutation RegisterOrganization($input: OrganizationInput!) {
      registerOrganization(input: $input) {
        id
        name
        email
        role
      }
    }
    """
    register_variables = {
        "input": {
            "name": "Test Org",
            "email": "testorg@example.com",
            "password": "securepassword",
            "role": "Organization"
        }
    }
    register_result = execute_graphql_query(client, register_mutation, register_variables)
    org = register_result["registerOrganization"]
    assert org["name"] == "Test Org"
    assert org["email"] == "testorg@example.com"
    
    # Test login
    login_mutation = """
    mutation LoginOrganization($input: LoginInput!) {
      loginOrganization(input: $input) {
        access_token
        token_type
      }
    }
    """
    login_variables = {
        "input": {
            "email": "testorg@example.com",
            "password": "securepassword"
        }
    }
    login_result = execute_graphql_query(client, login_mutation, login_variables)
    token_payload = login_result["loginOrganization"]
    assert "access_token" in token_payload
    assert token_payload["token_type"] == "bearer"

def test_verify_token_graphql(client):
    # First, register an organization to later verify the token.
    register_mutation = """
    mutation RegisterOrganization($input: OrganizationInput!) {
      registerOrganization(input: $input) {
        id
        email
      }
    }
    """
    register_variables = {
        "input": {
            "name": "Verify Org",
            "email": "verifyorg@example.com",
            "password": "mypassword",
            "role": "Policy Maker"
        }
    }
    _ = execute_graphql_query(client, register_mutation, register_variables)

    # Login to get a token
    login_mutation = """
    mutation LoginOrganization($input: LoginInput!) {
      loginOrganization(input: $input) {
        access_token
      }
    }
    """
    login_variables = {
        "input": {
            "email": "verifyorg@example.com",
            "password": "mypassword"
        }
    }
    login_result = execute_graphql_query(client, login_mutation, login_variables)
    token = login_result["loginOrganization"]["access_token"]
    
    # Verify token query
    verify_query = """
    query VerifyOrganizationToken($token: String!) {
      verifyOrganizationToken(token: $token) {
        email
      }
    }
    """
    verify_variables = {"token": token}
    verify_result = execute_graphql_query(client, verify_query, verify_variables)
    token_info = verify_result["verifyOrganizationToken"]
    assert token_info["email"] == "verifyorg@example.com"

def test_get_organization_by_email_graphql(client):
    # Register an organization.
    register_mutation = """
    mutation RegisterOrganization($input: OrganizationInput!) {
      registerOrganization(input: $input) {
        id
        email
      }
    }
    """
    register_variables = {
        "input": {
            "name": "Search Org",
            "email": "searchorg@example.com",
            "password": "searchpass",
            "role": "Organization"
        }
    }
    _ = execute_graphql_query(client, register_mutation, register_variables)
    
    # Query using getOrganizationByEmail
    query = """
    query GetOrganizationByEmail($email: String!) {
      getOrganizationByEmail(email: $email) {
        id
        name
        email
      }
    }
    """
    query_variables = {"email": "searchorg@example.com"}
    query_result = execute_graphql_query(client, query, query_variables)
    org = query_result["getOrganizationByEmail"]
    assert org["email"] == "searchorg@example.com"

