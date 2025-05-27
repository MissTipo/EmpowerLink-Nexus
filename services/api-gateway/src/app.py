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
# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Map GraphQL operation names to service endpoints
SERVICE_MAP = {
    # User Profile Service
    "getUserProfile": "http://user-profile:8001/graphql/",
    "createUserProfile": "http://user-profile:8001/graphql/",
    "updateUserProfile": "http://user-profile:8001/graphql/",
    "deleteUserProfile": "http://user-profile:8001/graphql",
    "deleteUserProfileByPhoneNumber": "http://user-profile:8001/graphql/",
    "allUserProfiles": "http://user-profile:8001/graphql",
    "getUserProfileByPhoneNumber": "http://user-profile:8001/graphql/",
    "getUserProfileByName": "http://user-profile:8001/graphql/",
    "getUsersByLocation": "http://user-profile:8001/graphql/",

    # Organization Profile Service
    "getOrganization": "http://organization-profile:8002/graphql/",
    "listOrganizations": "http://organization-profile:8002/graphql/",
    "signupOrganization": "http://organization-profile:8002/graphql/",
    "signinOrganization": "http://organization-profile:8002/graphql/",
    "updateOrganizationProfile": "http://organization-profile:8002/graphql/",

    # Telephony Integration Service
    "logIVRInteraction": "http://telephony-integration:8003/graphql/",
    "getUSSDMenu": "http://telephony-integration:8003/graphql/",
    # "dummy": "http://telephony-integration:8003/graphql/",
    # "dummyMutation": "http://telephony-integration:8003/graphql/",

    # Resource Matching Service
    "getMatchingResources": "http://resource-matching-service:8004/graphql/",
    "getAvailableResources": "http://resource-matching-service:8004/graphql/",
    "requestResourceMatching": "http://resource-matching-service:8004/graphql/",
    "createResource": "http://resource-matching-service:8004/graphql/",

    # Analytics & Reporting
    "resourcesPerCapita": "http://resource-matching-service:8004/graphql/",
    "resourceNeedGap": "http://resource-matching-service:8004/graphql/",
    "matchSuccessRate": "http://resource-matching-service:8004/graphql/",

    # Inclusivity Index Service
    "computeInclusivityIndex": "http://inclusivity-index-service:8006/graphql/",
    "updateInclusivityIndex": "http://inclusivity-index-service:8006/graphql/",
    "getTaskStatus": "http://inclusivity-index-service:8006/graphql/",

    # Geospatial Mapping Service
    "getResourceMap": "http://geospatial-mapping-service:8005/graphql/",
    "addResourceLocation": "http://geospatial-mapping-service:8005/graphql/",

    # Reporting & Feedback Service
    "getReports": "http://reporting-feedback-service:8007/graphql/",
    "submitReport": "http://reporting-feedback-service:8007/graphql/",
    "submitFeedback": "http://reporting-feedback-service:8007/graphql/",
}

@app.post("/graphql")
@app.post("/graphql/")
async def graphql_proxy(request: Request):
    # 1) Read the full JSON payload
    try:
        body = await request.json()
    except Exception as e:
        return JSONResponse(
            {"errors":[{"message": f"Invalid JSON body: {e}"}]},
            status_code=400
        )

    # 2) Log it for debugging (will show up in your pod logs)
    print("=== Incoming GraphQL Payload ===")
    print(body)
    print("================================")

    query = body.get("query", "")

    # 3) Pull out the very first field in the `{ ... }` selection set:
    m = re.search(r"\{\s*([A-Za-z0-9_]+)", query)
    # m = re.search(r"(?:query|mutation)?\s*[A-Za-z0-9_]*\s*\{\s*([A-Za-z0-9_]+)", query)

    if not m:
        return JSONResponse(
            {"errors":[{"message":"Could not determine selection field"}]},
            status_code=400
        )
    field = m.group(1)
    print(f"[Gateway] extracted field → {field!r}")

    # 4) Look up which service to call
    url = SERVICE_MAP.get(field)
    print(f"[Gateway] mapped URL     → {url!r}")
    if not url:
        return JSONResponse(
            {"errors":[{"message":f"Unknown operation: {field}"}]},
            status_code=400
        )
    print(f"[Gateway] mapped URL     → {url!r}")

    # 5) Forward the *entire* JSON body, including headers like Content-Type / Authorization
    headers = {
        "Content-Type": request.headers.get("content-type", "application/json"),
    }
    if auth := request.headers.get("authorization"):
        headers["Authorization"] = auth

    # Proxy the entire GraphQL payload
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.post(url, json=body, headers=headers, timeout=3600)
        try:
            data = resp.json()
        except Exception:
            data = {"errors":[{"message":"Invalid response from downstream"}]}
            return JSONResponse(content=data, status_code=502)
    return JSONResponse(content=data, status_code=resp.status_code)

@app.post("/ussd")
async def proxy_ussd(request: Request):
    # forward to the telephony service
    body = await request.body()
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://telephony-integration:8003/ussd",
            data=body,
            headers=request.headers.raw,
        )
    return PlainTextResponse(resp.text, status_code=resp.status_code)
