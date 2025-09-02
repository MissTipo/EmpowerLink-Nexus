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

def end_session(session_id, message):
    if session_id in USSD_SESSIONS:
        del USSD_SESSIONS[session_id]
    return f"END {message}"


@router.post("/ussd", response_class=PlainTextResponse)
async def ussd_callback(
    sessionId: str = Form(...),
    serviceCode: str = Form(...),
    phoneNumber: str = Form(...),
    text: str = Form(...)
):
    # initialize session if missing
    if sessionId not in USSD_SESSIONS:
        USSD_SESSIONS[sessionId] = {"step": 0}

    session = USSD_SESSIONS[sessionId]

    user_response = text.split("*") if text else []

    # Step 0: Initial request — no text submitted yet.
    if text == "":
        session["step"] = 0
        return "CON Welcome to EmpowerLink Nexus!\nPlease select your language:\n1. English\n2. Kiswahili"

    # Use step counter to track progress
    step = session.get("step", 0)

    # Step 1: Language selection
    if step == 0:
        selected_option = user_response[-1].strip()
        if selected_option not in ["1", "2"]:
            return "END Invalid selection. Goodbye."

        language = "English" if selected_option == "1" else "Kiswahili"
        session["language"] = language

        if phoneNumber in REGISTERED_USERS:
            # Already registered, jump to service menu
            session["step"] = 99  # special code for service menu directly
            return (f"CON Welcome back! (Language: {language})\n"
                    "1. Health Assistance\n2. Police & Justice Help\n3. Social Support")

        else:
            session["step"] = 1
            return f"CON Language set to {language}.\nTo register, please enter your name (or enter 0 to skip):"

    # Step 2: Collect Name
    elif step == 1:
        name_input = user_response[-1].strip()
        name = name_input if name_input and name_input != "0" else f"User_{phoneNumber[-4:]}"
        session["name"] = name
        session["step"] = 2
        return "CON Please enter your location:"

    # Step 3: Collect Location and Register
    elif step == 2:
        raw_loc = user_response[-1].strip()
        session["raw_location"] = raw_loc

        # 1) Ask geospatial-mapping service to resolve that raw input:
        try:
            async with httpx.AsyncClient() as client:
                geo_resp = await client.post(
                    settings.GEOMAP_URL + "/forward",  # or "/reverse" for lat/lon
                    json={"query": raw_loc}
                )
                geo_resp.raise_for_status()
                geo_data = geo_resp.json()

                # 2) Extract the cleaned place name and coords (adapt to your geo API shape)
                if geo_data.get("matches"):
                    match = geo_data["matches"][0]
                    place_name = match["name"]
                    coords     = match["coords"]          # e.g. {"lat": 1.23, "lon": 4.56}
                else:
                    place_name = raw_loc                  # fallback
                    coords     = None

        except Exception:
            # fallback if anything goes wrong
            place_name, coords = raw_loc, None

        session["location"] = place_name
        session["coords"]   = coords
        # location = user_response[-1].strip()
        # session["location"] = location
        #
        # name = session.get("name", f"User_{phoneNumber[-4:]}")
        # language = session.get("language", "English")

        mutation = """
        mutation CreateUserProfile($input: UserProfileInput!) {
          createUserProfile(input: $input) {
            id
            name
            phone_number
            location
            geo { lat lon }
          }
        }
        """
        variables = {
            "input": {
                "phone_number": phoneNumber,
                "name": session.get("name", f"User_{phoneNumber[-4:]}"),
                "location": place_name,
                "geo": coords,
                "gender": None,
                "age": None
            }
        }

        try:
            async with httpx.AsyncClient() as client:
                graphql_url = os.getenv("USER_PROFILE_GRAPHQL_URL", settings.USER_PROFILE_GRAPHQL_URL)
                gql_response = await client.post(graphql_url, json={"query": mutation, "variables": variables})
        except Exception as e:
            return f"END Registration error: {str(e)}"

        REGISTERED_USERS[phoneNumber] = {"name": session.get("name", f"User_{phoneNumber[-4:]}"), "location": place_name, "language": session.get("language", "en")}

        session["step"] = 99  # move to service menu
        return ("CON Registration successful!\n"
                "Service Menu:\n"
                "1. Health Assistance\n2. Police & Justice Help\n3. Social Support Services")

    # Step 4: Service Selection
    elif step == 99:
        option = user_response[-1].strip()
        if option == "1":
            return end_session(sessionId,"You selected Health Assistance. Our team will contact you shortly.")
        elif option == "2":
            return end_session(sessionId,"You selected Police & Justice Help. Assistance is on the way.")
        elif option == "3":
            return end_session(sessionId,"You selected Social Support Services. Please hold while we connect you.")
        else:
            return end_session(sessionId,"Invalid selection. Goodbye.")

    else:
        return end_session(sessionId,"Invalid input. Please try again.")

