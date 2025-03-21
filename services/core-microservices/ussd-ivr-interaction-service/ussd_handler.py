import json
from fastapi import Query
from fastapi.responses import PlainTextResponse
from utils.session_manager import get_session, update_session, clear_session
from utils.graphql_client import trigger_graphql_mutation

# Replace with your actual GraphQL endpoint URL
GRAPHQL_ENDPOINT = "http://api.yourdomain.com/graphql"

async def ussd_handler(
    SENDER: str = Query(..., description="Sender's phone number"),
    RECEIVER: str = Query(..., description="Receiver's service code"),
    SMS: str = Query(..., description="User input text")
) -> PlainTextResponse:
    session, session_key = await get_session(SENDER)
    step = session.get("step", 0)
    response_text = ""

    if step == 0:
        # Display main menu
        response_text = "Welcome to EmpowerLink Nexus:\n1. Report Incident\n2. Request Support"
        session["step"] = 1

    elif step == 1:
        # Process menu selection
        if SMS.strip() == "1":
            response_text = "You selected: Report Incident.\nPlease enter incident details:"
            session["step"] = 2
            session["action"] = "report_incident"
        elif SMS.strip() == "2":
            response_text = "You selected: Request Support.\nPlease enter your support request details:"
            session["step"] = 2
            session["action"] = "request_support"
        else:
            response_text = "Invalid selection. Please try again:\n1. Report Incident\n2. Request Support"

    elif step == 2:
        # Final step: Process details and trigger GraphQL mutation
        action = session.get("action")
        details = SMS.strip()
        trigger_graphql_mutation(action, details, SENDER, GRAPHQL_ENDPOINT)
        response_text = "Thank you. Your input has been submitted."
        await clear_session(session_key)
        return PlainTextResponse(response_text)

    # Update session state with a timeout of 300 seconds
    await update_session(session_key, session, timeout=300)
    return PlainTextResponse(response_text)

