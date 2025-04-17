# telephony-integration-service/app/ivr_routes.py

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.post("/ivr", response_class=PlainTextResponse)
async def ivr_callback():
    # For demonstration, a simple IVR response.
    response = ("CON Welcome to EmpowerLink Nexus IVR Service.\n"
                "Press 1 for Registration.\n"
                "Press 2 for Service Menu.")
    return response

