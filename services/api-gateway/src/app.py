import os
from fastapi import FastAPI
from ariadne import load_schema_from_path, make_executable_schema, QueryType, MutationType
from ariadne.asgi import GraphQL

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
from .resolvers.resource_resolver import resolve_requestResourceMatching
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
app.mount("/graphql", GraphQL(schema, debug=True))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

