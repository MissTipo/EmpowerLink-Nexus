# app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ariadne import load_schema_from_path, make_executable_schema, QueryType, MutationType
from ariadne.asgi import GraphQL

# Optional: import REST routes for auth if needed
from app.routes import router as auth_router

# Import GraphQL resolvers
from app.graphql.resolvers import (
    resolve_signupOrganization,
    resolve_signinOrganization,
    resolve_updateOrganizationProfile,
    resolve_getOrganization,
    resolve_listOrganizations,
)
from app.database import Base, engine

app = FastAPI(title="Organization Profile Service")

# CORS configuration (adjust origins as necessary)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST endpoints if needed (for auth, etc.)
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Create GraphQL type definitions
query = QueryType()
mutation = MutationType()

query.set_field("getOrganization", resolve_getOrganization)
query.set_field("listOrganizations", resolve_listOrganizations)
mutation.set_field("signupOrganization", resolve_signupOrganization)
mutation.set_field("signinOrganization", resolve_signinOrganization)
mutation.set_field("updateOrganizationProfile", resolve_updateOrganizationProfile)

schema_path = os.path.join(os.path.dirname(__file__), "graphql")
type_defs = load_schema_from_path(schema_path)

schema = make_executable_schema(type_defs, query, mutation)

# Mount GraphQL endpoint
app.mount("/graphql", GraphQL(schema, debug=True))
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True)

