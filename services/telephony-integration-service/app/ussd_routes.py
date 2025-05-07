# telephony-integration-service/app/ussd_routes.py

from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
import random
import httpx
import os
from config.settings import settings

router = APIRouter()

# In-memory session storage for demonstration.
USSD_SESSIONS = {}
REGISTERED_USERS = {}

@router.post("/ussd", response_class=PlainTextResponse)
async def ussd_callback(
    sessionId: str = Form(...),
    serviceCode: str = Form(...),
    phoneNumber: str = Form(...),
    text: str = Form(...)
):
    # 1) initialize session if missing
    if sessionId not in USSD_SESSIONS:
        USSD_SESSIONS[sessionId] = {}

    # 2) Work against a local reference
    session = USSD_SESSIONS[sessionId]

    """
    Simulates a USSD registration flow.
    Steps:
      0. On empty text: Display language selection.
      1. After language selection: If user not registered, ask for registration details; if registered, show service menu.
      2. Collect user name.
      3. Collect user location.
      4. Complete registration and display service menu.
    """
    # 3) if we've never asked language, show welcome
    if not session.get("asked_language"):
        session["phone"] = phoneNumber
        session["asked_language"] = True
        return "CON Welcome to EmpowerLink Nexus!\nPlease select your language:\n1. English\n2. Kiswahili"

    # 4) Now decide which prompt to send based on what keys are set:
    if "language" not in session:
        session["language"] = "English" if text.strip() == "1" else "Kiswahili"
        return f"CON Language set to {session['language']}.\nTo register, please enter your name (or 0 to skip):"

    if "name" not in session:
        # skip or collect name
        if text.strip() == "0":
            session["name"] = f"User_{phoneNumber[-4:]}"
        else:
            session["name"] = text.strip()
        return "CON Thank you. Auto-resolving your location now…"

    if "location" not in session:
        # call your geo service or assign default
        session["location"] = "Auto-Resolved City"
        # ... do your GraphQL mutation here ...
        return (
            "CON Registration successful!\n"
            "Service Menu:\n"
            "1. Health Assistance\n"
            "2. Police & Justice Help\n"
            "3. Social Support Services"
        )
    # Final menu choices
    option = text.strip()
    if option == "1":
        return "END You selected Health Assistance. Our team will contact you shortly."
    if option == "2":
        return "END You selected Police & Justice Help. Assistance is on the way."
    if option == "3":
        return "END You selected Social Support Services. Please hold while we connect you."
    return "END Invalid selection. Goodbye."

    # Step 0: Initial entry, show language selection if no text submitted.
    # if text == "":
    #     response = f"CON Welcome to EmpowerLink Nexus!\nPlease select your language:\n1. English\n2. Kiswahili"
    #     USSD_SESSIONS[sessionId] = {}
    #     return response
    #
    # # Parse the text inputs (using '*' as delimiter)
    # user_response = text.split("*")
    #
    # # Step 1: After language selection, record selected language and check registration.
    # if len(user_response) == 1:
    #     selected_option = user_response[0].strip()
    #     if selected_option not in ["1", "2"]:
    #         return "END Invalid selection. Goodbye."
    #     language = "English" if selected_option == "1" else "Kiswahili"
    #     USSD_SESSIONS[sessionId] = {"language": language}
    #     
    #     if phoneNumber in REGISTERED_USERS:
    #         # Already registered, show service menu.
    #         response = f"CON Welcome back! (Language: {language})\n1. Health Assistance\n2. Police & Justice Help\n3. Social Support"
    #     else:
    #         # Not registered, move to registration.
    #         response = f"CON Language set to {language}.\nTo register, please enter your name (or enter 0 to skip):"
    #     return response
    #
    # # Step 2: Collect Name.
    # if len(user_response) == 2:
    #     name_input = user_response[1].strip()
    #     name = name_input if name_input and name_input != "0" else f"User_{phoneNumber[-4:]}"
    #     USSD_SESSIONS[sessionId]["name"] = name
    #     response = "CON Please enter your location:"
    #     return response
    #
    # # Step 3: Collect Location and complete registration.
    # if len(user_response) == 3:
    #     location = user_response[2].strip()
    #     USSD_SESSIONS[sessionId]["location"] = location
    #
    #     # Retrieve data from the session store.
    #     name = USSD_SESSIONS[sessionId].get("name", f"User_{phoneNumber[-4:]}")
    #     language = USSD_SESSIONS[sessionId].get("language", "English")
    #     
    #     # Invoke the user profile creation via GraphQL.
    #     mutation = """
    #     mutation CreateUserProfile($input: UserProfileInput!) {
    #       createUserProfile(input: $input) {
    #         id
    #         name
    #         phone_number
    #         location
    #       }
    #     }
    #     """
    #     variables = {
    #         "input": {
    #             "phone_number": phoneNumber,
    #             "name": name,
    #             "location": location,
    #             # Additional fields can be added here.
    #             "gender": None,
    #             "age": None
    #         }
    #     }
    #     try:
    #         async with httpx.AsyncClient() as client:
    #             graphql_url = os.getenv("USER_PROFILE_GRAPHQL_URL", settings.USER_PROFILE_GRAPHQL_URL)
    #             gql_response = await client.post(graphql_url, json={"query": mutation, "variables": variables})
    #         # For simplicity, we assume registration is successful.
    #     except Exception as e:
    #         return f"END Registration error: {str(e)}"
    #     
    #     # Mark user as registered.
    #     REGISTERED_USERS[phoneNumber] = {"name": name, "location": location, "language": language}
    #     
    #     # Proceed to Service Menu.
    #     response = ("CON Registration successful!\n"
    #                 "Service Menu:\n"
    #                 "1. Health Assistance\n"
    #                 "2. Police & Justice Help\n"
    #                 "3. Social Support Services")
    #     return response
    #
    # Step 4: Handle Service Selection if the user is already registered.
    # if len(user_response) >= 4:
    #     option = user_response[3].strip()
    #     if option == "1":
    #         return "END You selected Health Assistance. Our team will contact you shortly."
    #     elif option == "2":
    #         return "END You selected Police & Justice Help. Assistance is on the way."
    #     elif option == "3":
    #         return "END You selected Social Support Services. Please hold while we connect you."
    #     else:
    #         return "END Invalid selection. Goodbye."
    #
    # return "END Invalid input. Please try again."
    #
