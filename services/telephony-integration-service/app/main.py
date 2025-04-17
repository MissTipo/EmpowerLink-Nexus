# telephony-integration-service/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import USSD and IVR routers
from app.ussd_routes import router as ussd_router
from app.ivr_routes import router as ivr_router

# Optional: Import GraphQL if you want to expose any telephony-specific mutations/queries
from ariadne.asgi import GraphQL
from ariadne import load_schema_from_path, make_executable_schema, QueryType, MutationType
from app.graphql.resolvers import resolve_dummy, resolve_dummy_mutation

app = FastAPI(title="Telephony Integration Service")

# Global CORS settings (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include USSD and IVR routes
app.include_router(ussd_router, prefix="")
app.include_router(ivr_router, prefix="")

# (Optional) Set up a simple GraphQL endpoint, if desired for internal use.
query = QueryType()
mutation = MutationType()
query.set_field("dummy", resolve_dummy)
mutation.set_field("dummyMutation", resolve_dummy_mutation)
schema_path = "app/graphql"  # Assumes your schema.graphql is under app/graphql
type_defs = load_schema_from_path(schema_path)
schema = make_executable_schema(type_defs, query, mutation)
app.mount("/graphql", GraphQL(schema, debug=True))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True)

