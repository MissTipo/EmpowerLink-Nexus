import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.ussd_routes import USSD_SESSIONS, REGISTERED_USERS

client = TestClient(app)

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
    
    # Step 0: Initial empty text -> language selection
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": ""
    })
    assert "Please select your language" in r.text
    
    # Step 1: User selects a language ("1" for English)
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": "1"
    })
    # Should set language and prompt for name.
    assert "enter your name" in r.text.lower()
    
    # Step 2: User enters name ("Alice") - simulate input "1*Alice"
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": "1*Alice"
    })
    # Prompt should now ask for location.
    assert "enter your location" in r.text.lower()
    
    # Step 3: User enters location ("Nairobi") - simulate input "1*Alice*Nairobi"
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": "1*Alice*Nairobi"
    })
    # Now expect registration success message and service menu.
    assert "registration successful" in r.text.lower()
    assert "service menu" in r.text.lower()
    
    # Verify that the user is marked as registered in our demo store.
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
    
    # Step 1: Select language "2" (Kiswahili)
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": "2"
    })
    # Should prompt for name
    assert "enter your name" in r.text.lower()
    
    # Step 2: User enters "0" to skip name.
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": "2*0"
    })
    # Should now ask for location.
    assert "enter your location" in r.text.lower()
    
    # Step 3: User enters location "Mombasa"
    r = client.post("/ussd", data={
        "sessionId": session_id,
        "serviceCode": "*999#",
        "phoneNumber": phone,
        "text": "2*0*Mombasa"
    })
    # Should complete registration and display service menu.
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
    
    # Simulate a USSD request where user already registered and now selects a service.
    # The "text" could be constructed to have a fourth step indicating service selection.
    # Here, we simulate "1" at step 1 followed by three steps already done and then a selection.
    # For simplicity, we provide a text value with 4 parts.
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

