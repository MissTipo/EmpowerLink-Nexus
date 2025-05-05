import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL

from app.database import Base, engine
from app.routes import router as inclusivity_router
from app.graphql.resolvers import query

app = FastAPI(title="Inclusivity Index Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount REST endpoints
app.include_router(inclusivity_router)

# mount GraphQL
schema_dir = os.path.join(os.path.dirname(__file__), "graphql")
type_defs   = load_schema_from_path(schema_dir)
schema      = make_executable_schema(type_defs, query)
app.mount("/graphql", GraphQL(schema, debug=True))

# create tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8006, reload=True)

