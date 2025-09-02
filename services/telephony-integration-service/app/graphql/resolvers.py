# telephony‑integration‑service/app/graphql/resolvers.py

from ariadne import QueryType, MutationType
import httpx
import os
from config.settings import settings

query = QueryType()
mutation = MutationType()

@query.field("getUSSDMenu")
async def resolve_get_ussd_menu(_, info, phoneNumber, input):
    """
    Forwards the GraphQL call into your existing FastAPI /ussd endpoint
    """
    # Build the USSD POST form
    form = {
        "sessionId":   info.context["request"].headers.get("X-USSD-Session-Id", phoneNumber),
        "serviceCode": info.context["request"].headers.get("X-USSD-Service-Code", settings.USSD_CODE),
        "phoneNumber":    phoneNumber,
        "text":           input or ""
    }

    ussd_url = settings.USSD_CALLBACK_URL
    async with httpx.AsyncClient() as client:
        resp = await client.post(ussd_url, data=form)
        resp.raise_for_status()

    return {"message": resp.text}

@query.field("dummy")
def resolve_dummy(_, info):
    return "dummy response"

@mutation.field("dummyMutation")
def resolve_dummy_mutation(_, info):
    return "dummy mutation response"
