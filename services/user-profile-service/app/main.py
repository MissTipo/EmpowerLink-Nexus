# user-profile-service/app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ariadne import load_schema_from_path, make_executable_schema, QueryType, MutationType
from ariadne.asgi import GraphQL

# Import REST routes (if used)
from app.routes import router as user_router

# Import GraphQL resolvers
from app.graphql.resolvers import (
    resolve_getUserProfile,
    resolve_createUserProfile,
    resolve_updateUserProfile,
)

# Initialize FastAPI app
app = FastAPI(title="User Profile Service")

# Optional: add CORS settings if this service will be called from other origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount REST routes (if you plan on using REST endpoints as well)
app.include_router(user_router, prefix="/api/users")

# Create GraphQL Query and Mutation types
query = QueryType()
mutation = MutationType()

# Map GraphQL resolvers (example for user profiles)
query.set_field("getUserProfile", resolve_getUserProfile)
mutation.set_field("createUserProfile", resolve_createUserProfile)
mutation.set_field("updateUserProfile", resolve_updateUserProfile)

# Load GraphQL schema from file
schema_path = os.path.join(os.path.dirname(__file__), "graphql")
type_defs = load_schema_from_path(schema_path)

schema = make_executable_schema(type_defs, query, mutation)

# Mount GraphQL endpoint at /graphql
app.mount("/graphql", GraphQL(schema, debug=True))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)

