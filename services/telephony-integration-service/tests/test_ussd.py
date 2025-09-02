import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.ussd_routes import USSD_SESSIONS, REGISTERED_USERS

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_state():
    # before each test
    USSD_SESSIONS.clear()
    REGISTERED_USERS.clear()
    yield
    # after each test
    USSD_SESSIONS.clear()
    REGISTERED_USERS.clear()

def test_initial_menu():
    # When text is empty, expect language selection.
    response = client.post(
        "/ussd",
        data={
            "sessionId": "sess1",
            "serviceCode": "*999#",
            "phoneNumber": "+254712345678",
            "text": ""
        }
    )
    # Should prompt language selection.
    assert response.status_code == 200
    assert "Please select your language" in response.text
    # Reset session store for isolation.
    USSD_SESSIONS.clear()
    REGISTERED_USERS.clear()

def test_language_selection_and_registration_flow():
    session_id = "sess2"
    phone = "+254712345678"
    
    # Initial empty text -> language selection
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": ""
    })
    assert "Please select your language" in r.text
    
    # User selects a language ("1" for English)
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": "1"
    })
    # Should set language and prompt for name.
    assert "enter your name" in r.text.lower()
    
    # User enters name ("Alice") - simulate input "1*Alice"
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": "1*Alice"
    })
    assert "enter your location" in r.text.lower()
    
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": "1*Alice*Nairobi"
    })
    assert "registration successful" in r.text.lower()
    assert "service menu" in r.text.lower()
    
    # Verify that the user is marked as registered in the demo store.
    assert phone in REGISTERED_USERS
    assert REGISTERED_USERS[phone]["name"] == "Alice"
    assert REGISTERED_USERS[phone]["location"] == "Nairobi"

def test_registration_with_no_name():
    session_id = "sess3"
    phone = "+254712345679"
    
    # Step 0: Initial empty text -> language selection
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": ""
    })
    assert "please select your language" in r.text.lower()
    
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": "2"
    })
    assert "enter your name" in r.text.lower()
    
    # If user enters "0" to skip name.
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": "2*0"
    })
    # Should prompt for location.
    assert "enter your location" in r.text.lower()
    
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": "2*0*Mombasa"
    })
    # Complete registration and display service menu.
    assert "registration successful" in r.text.lower()
    
    # Check that a default name was assigned.
    registered = REGISTERED_USERS.get(phone, {})
    assert "name" in registered
    assert registered["name"].startswith("User_")
    assert registered["location"] == "Mombasa"

def test_service_menu_selection():
    # Assume the user is already registered.
    session_id = "sess4"
    phone = "+254712345680"
    REGISTERED_USERS[phone] = {"name": "Bob", "location": "Nairobi", "language": "English"}
    
    """
    Simulate a USSD request where user already registered and now selects a service.
    The "text" could be constructed to have a fourth step indicating service selection.
    Here, we simulate "1" at step 1 followed by three steps already done and then a selection.
    For simplicity, we provide a text value with 4 parts.
    """

    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": "1*Bob*Nairobi*1"
    })
    # Expect an END response with the corresponding service message.
    assert "health assistance" in r.text.lower() or \
           "police" in r.text.lower() or \
           "social support" in r.text.lower() or \
           "invalid selection" in r.text.lower()


def test_invalid_language_selection():
    """If user enters something other than 1 or 2 on first prompt, we END."""
    r = client.post("/ussd", data={
        "sessionId": "s1", "serviceCode": "*999#", "phoneNumber": "+100", "text": "9"
    })
    assert r.text.startswith("END")
    assert "Invalid selection" in r.text

def test_skip_name_assigns_default_and_still_registers(monkeypatch):
    """Make sure that skipping name (enter 0) still stores a User_xxxx default name."""
    # Step0 -> language
    client.post("/ussd", data={"sessionId":"s2","serviceCode":"*999#","phoneNumber":"+200","text":""})
    # Step1 -> select language English
    client.post("/ussd", data={"sessionId":"s2","serviceCode":"*999#","phoneNumber":"+200","text":"1"})
    # Step2 -> skip name "0"
    client.post("/ussd", data={
        "sessionId":"s2","serviceCode":"*999#","phoneNumber":"+200","text":"1*0"
    })
    # Now register location Mombasa -> we need to mock the GraphQL call so it doesn't actually fire
    async def fake_post(self, url, *, data=None, json=None, **kwargs):
        class FakeResp:
            status_code=200
            text=""
            def raise_for_status(self): pass
        return FakeResp()
    monkeypatch.setattr("app.ussd_routes.httpx.AsyncClient.post", fake_post)
    
    r = client.post("/ussd", data={
        "sessionId":"s2","serviceCode":"*999#","phoneNumber":"+200","text":"1*0*Mombasa"
    })
    assert "Registration successful" in r.text
    # user stored
    stored = REGISTERED_USERS["+200"]
    assert stored["location"] == "Mombasa"
    assert stored["name"].startswith("User_")
    assert stored["language"] == "English"

def test_service_menu_after_registration():
    """After full registration, selecting service '2' returns Police & Justice."""
    phone = "+300"
    session_id = "s3"

    REGISTERED_USERS[phone] = {"name": "Zoe", "location": "Nairobi", "language": "English"}

    # Starting the session
    client.post("/ussd", data={
        "sessionId": session_id, "serviceCode": "*999#", "phoneNumber": phone, "text": ""
    })

    # Selecting language
    client.post("/ussd", data={
        "sessionId": session_id, "serviceCode": "*999#", "phoneNumber": phone, "text": "1"
    })

    # Selecting service option 2
    r = client.post("/ussd", data={
        "sessionId": session_id, "serviceCode": "*999#", "phoneNumber": phone, "text": "1*2"
    })

    assert r.text.startswith("END")
    assert "Police & Justice" in r.text

def test_dummy_graphql_query_and_mutation():
    """Exercise the GraphQL (/graphql) dummy resolvers."""
    # query
    resp_q = client.post("/graphql", json={"query":"{ dummy }"})
    assert resp_q.status_code == 200
    assert resp_q.json()["data"]["dummy"] == "dummy response"
    # mutation
    resp_m = client.post("/graphql", json={"query":"mutation { dummyMutation }"})
    assert resp_m.status_code == 200
    assert resp_m.json()["data"]["dummyMutation"] == "dummy mutation response"
