import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ariadne import load_schema_from_path, make_executable_schema, QueryType
from ariadne.asgi import GraphQL

from app.routes import router as map_router
from app.database import Base, engine
from app.graphql.resolvers import resolve_all_locations, resolve_service_deserts

app = FastAPI(title="Geospatial Mapping Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST under /map
app.include_router(map_router, prefix="/map", tags=["mapping"])

# GraphQL
query = QueryType()
query.set_field("allResourceLocations", resolve_all_locations)
query.set_field("serviceDeserts", resolve_service_deserts)

schema_dir = os.path.join(os.path.dirname(__file__), "graphql")
type_defs = load_schema_from_path(schema_dir)
schema = make_executable_schema(type_defs, query)

app.mount("/graphql", GraphQL(schema, debug=True))

# ensure tables exist
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

