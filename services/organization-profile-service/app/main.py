import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ariadne import load_schema_from_path, make_executable_schema, QueryType, MutationType
from ariadne.asgi import GraphQL

from app.routes import router as org_router
from app.graphql.resolvers import (
    resolve_registerOrganization,
    resolve_loginOrganization,
    resolve_verifyOrganizationToken,
    resolve_getOrganizationByEmail,
)
from app.database import Base, engine

app = FastAPI(title="Organization Auth Service")

# Add CORS middleware (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount REST routes (if you plan on using them)
app.include_router(org_router, prefix="/api/org")

# Create GraphQL Query and Mutation types
query = QueryType()
mutation = MutationType()

# Map GraphQL resolvers to their corresponding query/mutation fields
query.set_field("getOrganizationByEmail", resolve_getOrganizationByEmail)
mutation.set_field("registerOrganization", resolve_registerOrganization)
mutation.set_field("loginOrganization", resolve_loginOrganization)
mutation.set_field("verifyOrganizationToken", resolve_verifyOrganizationToken)

# Load the GraphQL schema from the 'graphql' folder
schema_path = os.path.join(os.path.dirname(__file__), "graphql")
type_defs = load_schema_from_path(schema_path)
schema = make_executable_schema(type_defs, query, mutation)

# Mount GraphQL endpoint at /graphql
app.mount("/graphql", GraphQL(schema, debug=True))

# Create all tables (useful for development; in production, use migrations)
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True)

