import requests
from ariadne import MutationType, QueryType, make_executable_schema, load_schema_from_path
from app.models import Resource
from app.schemas import ResourceOut
from app.database import SessionLocal
from config.settings import settings

# Initialize the Query and Mutation types
query = QueryType()
mutation = MutationType()

# Define a mapping from role to service type
ROLE_TO_SERVICE_TYPE = {
    "health": "HEALTH",
    "legal": "LEGAL",
    "social": "SOCIAL"
}

# URL of the organization service's endpoint
ORGANIZATION_SERVICE_URL = "http://35.238.68.232.nip.io/graphql"

@mutation.field("createResource")
def resolve_create_resource(_, info, organizationId, input):
    db = SessionLocal()

    # Fetch the organization by ID from the organization service
    response = requests.get(f"{ORGANIZATION_SERVICE_URL}{organizationId}")
    
    if response.status_code != 200:
        db.close()
        raise Exception("Organization not found or error fetching organization details")

    organization = response.json()  # Assuming the organization details are returned as JSON

    # Derive the service_type based on the role
    service_type = ROLE_TO_SERVICE_TYPE.get(organization['role'].lower())
    if not service_type:
        db.close()
        raise Exception("Service type not found for the given role")

    # Create the new resource linked to the organization
    new_resource = Resource(
        service_type=service_type,
        organization_id=organizationId,  # Store the organizationId
        **input  # Unpack input data for latitude, longitude, etc.
    )

    # Add to the database
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    db.close()

    # Return the created resource
    return ResourceOut.from_orm(new_resource)

# ─── Queries ────────────────────────────────────────────────────────────────

@query.field("getAvailableResources")
def resolve_get_available_resources(_, info, serviceType=None, limit=50):
    """
    Returns up to `limit` resources, optionally filtering by serviceType.
    """
    db = SessionLocal()
    q = db.query(Resource)
    if serviceType:
        q = q.filter(Resource.service_type == serviceType.lower())
    resources = q.limit(limit).all()
    db.close()
    return [ResourceOut.from_orm(r) for r in resources]

@query.field("requestResourceMatching")
def resolve_request_resource_matching(_, info, **kwargs):
    """
    Alias to getMatchingResources—runs the matching logic and returns the same shape.
    """
    # reuse your existing matching logic
    matches = match_resources(kwargs, limit=kwargs.get("limit", settings.knn_n_neighbors))
    db = SessionLocal()
    out = []
    for m in matches:
        r = db.query(Resource).get(m["resource_id"])
        out.append(
            ResourceMatch(
                resource=ResourceOut.from_orm(r),
                score=1 / (1 + m["distance"])
            )
        )
    db.close()
    return out
