# telephony-integration-service/app/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

# Import USSD and IVR routers
from app.ussd_routes import router as ussd_router
from app.ivr_routes import router as ivr_router

# GraphQL imports
from ariadne import load_schema_from_path, make_executable_schema, QueryType
from ariadne.asgi import GraphQL
from ariadne import load_schema_from_path, make_executable_schema, QueryType, MutationType
from app.graphql.resolvers import resolve_dummy, resolve_dummy_mutation
from app.graphql.resolvers import query as graphql_query, mutation as graphql_mutation

app = FastAPI(title="Telephony Integration Service")

# Global CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1) Include USSD and IVR routes
app.include_router(ussd_router, prefix="")
app.include_router(ivr_router, prefix="")

# 2) GraphQL schema + resolvers
schema_path = os.path.join(os.path.dirname(__file__), "graphql")
type_defs = load_schema_from_path(schema_path)
schema = make_executable_schema(type_defs, [graphql_query, graphql_mutation])

# 3) Mount at /graphql
app.mount("/graphql", GraphQL(schema, debug=True))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8003, reload=True)

