# api-gateway/src/app.py
import re
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from ariadne import load_schema_from_path, make_executable_schema, QueryType, MutationType
from ariadne.asgi import GraphQL
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import httpx

app = FastAPI(title="EmpowerLink Nexus API Gateway")

# CORS settings: allow from all origins or restrict as needed
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Map GraphQL operation names to service endpoints
SERVICE_MAP = {
    # User Profile Service
    "getUserProfile": "http://user-profile:8001/graphql",
    "createUserProfile": "http://user-profile:8001/graphql",
    "updateUserProfile": "http://user-profile:8001/graphql",
    "deleteUserProfile": "http://user-profile:8001/graphql",
    "deleteUserProfileByPhoneNumber": "http://user-profile:8001/graphql",
    "allUserProfiles": "http://user-profile:8001/graphql",
    "getUserProfileByPhoneNumber": "http://user-profile:8001/graphql",
    "getUserProfileByName": "http://user-profile:8001/graphql",
    "getUsersByLocation": "http://user-profile:8001/graphql",

    # Organization Profile Service
    "getOrganization": "http://organization-profile:8002/graphql",
    "listOrganizations": "http://organization-profile:8002/graphql",
    "signupOrganization": "http://organization-profile:8002/graphql",
    "signinOrganization": "http://organization-profile:8002/graphql",
    "updateOrganizationProfile": "http://organization-profile:8002/graphql",

    # Telephony Integration Service
    "logIVRInteraction": "http://telephony-integration:8003/graphql",
    "getUSSDMenu": "http://telephony-integration:8003/graphql",
    "dummy": "http://telephony-integration:8003/graphql",
    "dummyMutation": "http://telephony-integration:8003/graphql",

    # Resource Matching Service
    "getMatchingResources": "http://resource-matching-service:8004/graphql",
    "getAvailableResources": "http://resource-matching-service:8004/graphql",
    "requestResourceMatching": "http://resource-matching-service:8004/graphql",

    # Inclusivity Index Service
    "getInclusivityIndex": "http://inclusivity-index-service:8005/graphql",
    "updateInclusivityIndex": "http://inclusivity-index-service:8005/graphql",

    # Geospatial Mapping Service
    "getResourceMap": "http://geospatial-mapping-service:8006/graphql",
    "addResourceLocation": "http://geospatial-mapping-service:8006/graphql",

    # Reporting & Feedback Service
    "getReports": "http://reporting-feedback-service:8007/graphql",
    "submitReport": "http://reporting-feedback-service:8007/graphql",
    "submitFeedback": "http://reporting-feedback-service:8007/graphql",
}

@app.post("/graphql")
async def graphql_proxy(request: Request):
    body = await request.json()
    query = body.get("query", "")

    # Pull out the very first field in the `{ ... }` selection set:
    # m = re.search(r"\{\s*([A-Za-z0-9_]+)", query)
    m = re.search(r"(?:query|mutation)?\s*[A-Za-z0-9_]*\s*\{\s*([A-Za-z0-9_]+)", query)

    if not m:
        return JSONResponse(
            {"errors":[{"message":"Could not determine selection field"}]},
            status_code=400
        )
    field = m.group(1)

    # Look up which service to call
    url = SERVICE_MAP.get(field)
    if not url:
        return JSONResponse(
            {"errors":[{"message":f"Unknown operation: {field}"}]},
            status_code=400
        )

    # Proxy the entire GraphQL payload
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=body)
        try:
            data = resp.json()
        except ValueError:
            data = {"errors":[{"message":"Invalid response from downstream"}]}
    return JSONResponse(content=data, status_code=resp.status_code)

