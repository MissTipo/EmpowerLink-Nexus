import json
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Helper function to execute GraphQL queries/mutations
def execute_query(query: str, variables: dict = None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = client.post("/graphql", json=payload)
    assert response.status_code == 200, f"Response status code: {response.status_code}"
    result = response.json()
    assert "errors" not in result, f"GraphQL errors: {result.get('errors')}"
    return result["data"]

# ------------------------------
# Query Tests
# ------------------------------

def test_get_user_profile():
    query = """
    query {
      getUserProfile(id: "1") {
        id
        name
        gender
        age
        location
      }
    }
    """
    data = execute_query(query)
    user = data["getUserProfile"]
    assert user["id"] == "1"
    assert user["name"] == "John Doe"
    # Additional assertions as per resolver implementation

def test_get_available_resources():
    query = """
    query {
      getAvailableResources {
        id
        type
        description
        location
      }
    }
    """
    data = execute_query(query)
    resources = data["getAvailableResources"]
    # As our dummy resolver returns an empty list:
    assert isinstance(resources, list)
    assert len(resources) == 0

def test_get_inclusivity_index():
    query = """
    query {
      getInclusivityIndex {
        score
        genderEquity
        accessToLegalAid
      }
    }
    """
    data = execute_query(query)
    index = data["getInclusivityIndex"]
    assert isinstance(index["score"], float)
    assert isinstance(index["genderEquity"], float)
    assert isinstance(index["accessToLegalAid"], float)

def test_get_resource_map():
    query = """
    query getResourceMap($location: LocationInput!) {
      getResourceMap(location: $location) {
        resourceId
        latitude
        longitude
        available
      }
    }
    """
    variables = {"location": {"latitude": 0.0, "longitude": 0.0}}
    data = execute_query(query, variables)
    resource_map = data["getResourceMap"]
    assert isinstance(resource_map, list)

def test_get_reports():
    query = """
    query {
      getReports {
        id
        userId
        type
        description
        createdAt
      }
    }
    """
    data = execute_query(query)
    reports = data["getReports"]
    assert isinstance(reports, list)

def test_get_ussd_menu():
    query = """
    query {
      getUSSDMenu {
        id
        title
        description
      }
    }
    """
    data = execute_query(query)
    menu = data["getUSSDMenu"]
    assert isinstance(menu, list)

# ------------------------------
# Mutation Tests
# ------------------------------

def test_create_user_profile():
    mutation = """
    mutation CreateUserProfile($input: UserProfileInput!) {
      createUserProfile(input: $input) {
        id
        name
        gender
        age
        location
      }
    }
    """
    variables = {"input": {"name": "Alice", "gender": "Female", "age": 28, "location": "CityX"}}
    data = execute_query(mutation, variables)
    profile = data["createUserProfile"]
    assert profile["name"] == "Alice"
    assert profile["gender"] == "Female"
    assert profile["age"] == 28
    assert profile["location"] == "CityX"

def test_update_user_profile():
    mutation = """
    mutation UpdateUserProfile($id: ID!, $input: UserProfileInput!) {
      updateUserProfile(id: $id, input: $input) {
        id
        name
        gender
        age
        location
      }
    }
    """
    variables = {"id": "1", "input": {"name": "Alice Updated", "gender": "Female", "age": 29, "location": "CityY"}}
    data = execute_query(mutation, variables)
    profile = data["updateUserProfile"]
    assert profile["id"] == "1"
    assert profile["name"] == "Alice Updated"

def test_request_resource_matching():
    mutation = """
    mutation {
      requestResourceMatching(userId: "1", resourceId: "101") {
        userId
        resourceId
        matchedAt
      }
    }
    """
    data = execute_query(mutation)
    match = data["requestResourceMatching"]
    assert match["userId"] == "1"
    assert match["resourceId"] == "101"

def test_update_inclusivity_index():
    mutation = """
    mutation UpdateInclusivityIndex($data: InclusivityDataInput!) {
      updateInclusivityIndex(data: $data) {
        score
        genderEquity
        accessToLegalAid
      }
    }
    """
    variables = {"data": {"score": 75.0, "genderEquity": 80.0, "accessToLegalAid": 70.0}}
    data = execute_query(mutation, variables)
    index = data["updateInclusivityIndex"]
    assert index["score"] == 75.0
    assert index["genderEquity"] == 80.0
    assert index["accessToLegalAid"] == 70.0

def test_add_resource_location():
    mutation = """
    mutation AddResourceLocation($input: ResourceLocationInput!) {
      addResourceLocation(input: $input) {
        resourceId
        latitude
        longitude
        available
      }
    }
    """
    variables = {"input": {"resourceId": "201", "latitude": 45.0, "longitude": -93.0, "available": True}}
    data = execute_query(mutation, variables)
    location = data["addResourceLocation"]
    assert location["resourceId"] == "201"
    assert location["latitude"] == 45.0

def test_submit_report():
    mutation = """
    mutation SubmitReport($input: ReportInput!) {
      submitReport(input: $input) {
        id
        userId
        type
        description
        createdAt
      }
    }
    """
    variables = {"input": {"userId": "1", "type": "Incident", "description": "Test report"}}
    data = execute_query(mutation, variables)
    report = data["submitReport"]
    assert report["userId"] == "1"
    assert report["type"] == "Incident"

def test_submit_feedback():
    mutation = """
    mutation SubmitFeedback($input: FeedbackInput!) {
      submitFeedback(input: $input) {
        id
        userId
        feedback
        createdAt
      }
    }
    """
    variables = {"input": {"userId": "1", "feedback": "Test feedback"}}
    data = execute_query(mutation, variables)
    feedback = data["submitFeedback"]
    assert feedback["userId"] == "1"
    assert feedback["feedback"] == "Test feedback"

def test_log_ivr_interaction():
    mutation = """
    mutation LogIVRInteraction($input: IVRInteractionInput!) {
      logIVRInteraction(input: $input) {
        userId
        interactionType
        details
      }
    }
    """
    variables = {"input": {"userId": "1", "interactionType": "Call", "details": "IVR test call"}}
    data = execute_query(mutation, variables)
    interaction = data["logIVRInteraction"]
    assert interaction["userId"] == "1"
    assert interaction["interactionType"] == "Call"

