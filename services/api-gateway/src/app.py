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
    "getUserProfile": "http://user-profile-service:8001/graphql",
    "createUserProfile": "http://user-profile-service:8001/graphql",
    "updateUserProfile": "http://user-profile-service:8001/graphql",
    "deleteUserProfile": "http://user-profile-service:8001/graphql",
    "deleteUserProfileByPhoneNumber": "http://user-profile-service:8001/graphql",
    "allUserProfiles": "http://user-profile-service:8001/graphql",
    "getUserProfileByPhoneNumber": "http://user-profile-service:8001/graphql",
    "getUserProfileByName": "http://user-profile-service:8001/graphql",
    "getUsersByLocation": "http://user-profile-service:8001/graphql",

    # Organization Profile Service
    "getOrganization": "http://organization-profile-service:8002/graphql",
    "listOrganizations": "http://organization-profile-service:8002/graphql",
    "signupOrganization": "http://organization-profile-service:8002/graphql",
    "signinOrganization": "http://organization-profile-service:8002/graphql",
    "updateOrganizationProfile": "http://organization-profile-service:8002/graphql",

    # Telephony Integration Service
    "logIVRInteraction": "http://telephony-integration-service:8003/graphql",
    "getUSSDMenu": "http://telephony-integration-service:8003/graphql",
    "dummy": "http://telephony-integration-service:8003/graphql",
    "dummyMutation": "http://telephony-integration-service:8003/graphql",

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


"""
# Import resolvers from the resolvers directory
from .resolvers.query_resolver import (
    resolve_getUserProfile,
    resolve_getMatchingResources,
    resolve_getAvailableResources,
    resolve_getInclusivityIndex,
    resolve_getResourceMap,
    resolve_getReports,
    resolve_getUSSDMenu,
)
from .resolvers.feedback_resolver import resolve_submitReport, resolve_submitFeedback
from .resolvers.inclusivity_resolver import resolve_updateInclusivityIndex
from .resolvers.resource_resolver import resolve_requestResourceMatching, resolve_addResource
from .resolvers.geospatial_resolver import resolve_addResourceLocation
from .resolvers.telephony_resolver import resolve_logIVRInteraction

# Create the Query and Mutation types
query = QueryType()
mutation = MutationType()

# Map Query resolvers
query.set_field("getUserProfile", resolve_getUserProfile)
query.set_field("getMatchingResources", resolve_getMatchingResources)
query.set_field("getAvailableResources", resolve_getAvailableResources)
query.set_field("getInclusivityIndex", resolve_getInclusivityIndex)
query.set_field("getResourceMap", resolve_getResourceMap)
query.set_field("getReports", resolve_getReports)
query.set_field("getUSSDMenu", resolve_getUSSDMenu)

# Map Mutation resolvers
mutation.set_field("createUserProfile", lambda obj, info, input: {"id": "1", **input})
mutation.set_field("updateUserProfile", lambda obj, info, id, input: {"id": id, **input})
mutation.set_field("requestResourceMatching", resolve_requestResourceMatching)
mutation.set_field("updateInclusivityIndex", resolve_updateInclusivityIndex)
mutation.set_field("addResourceLocation", resolve_addResourceLocation)
mutation.set_field("addResource", resolve_addResource)
mutation.set_field("submitReport", resolve_submitReport)
mutation.set_field("submitFeedback", resolve_submitFeedback)
mutation.set_field("logIVRInteraction", resolve_logIVRInteraction)

# Load all .graphql files from the schema directory
schema_path = os.path.join(os.path.dirname(__file__), "schema")
type_defs = load_schema_from_path(schema_path)

# Create the executable schema
schema = make_executable_schema(type_defs, query, mutation)

# Initialize FastAPI and mount the GraphQL app
app = FastAPI()

# Add CORS middleware to allow requests from localhost:3000
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

app.mount("/graphql", GraphQL(schema, debug=True))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
