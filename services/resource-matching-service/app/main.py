import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ariadne.asgi import GraphQL
from ariadne import load_schema_from_path, make_executable_schema

from app.routes import router as rest_router
from app.graphql import resolvers
from app.database import Base, engine

app = FastAPI(title="Resource Matching Service")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST endpoints
app.include_router(rest_router)

# Setup GraphQL
schema = make_executable_schema(
    load_schema_from_path(os.path.join(os.path.dirname(__file__), "graphql", "schema.graphql")),
    resolvers.query,
    resolvers.mutation
)
app.mount("/graphql", GraphQL(schema, debug=True))

# Create DB tables at startup
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8004, reload=True)

