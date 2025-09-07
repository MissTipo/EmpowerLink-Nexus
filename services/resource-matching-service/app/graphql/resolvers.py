import requests
import datetime
from sqlalchemy import func, Integer, cast
from ariadne import MutationType, QueryType, make_executable_schema, load_schema_from_path
from app.models import Resource, Region, DemandLog, MatchLog
from app.schemas import ResourceOut
from app.database import SessionLocal
from config.settings import settings
from ai.matching_model import match_resources

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
ORGANIZATION_SERVICE_URL = "http://organization-profile:8002/graphql"

@mutation.field("createResource")
def resolve_create_resource(_, info, organizationId, input):
    db = SessionLocal()

    # Build the GraphQL query
    graphql_query = {
        "query": """
            query ($id: ID!) {
                getOrganization(id: $id) {
                    id
                    name
                    role
                }
            }
        """,
        "variables": {"id": organizationId}
    }

    try:
        # Make the GraphQL POST request to organization service
        response = requests.post(
            ORGANIZATION_SERVICE_URL,
            json=graphql_query
        )
        response.raise_for_status()
        data = response.json()

        # Error handling
        if "errors" in data:
            raise Exception(f"GraphQL error: {data['errors']}")

        organization = data["data"]["getOrganization"]
        if not organization:
            raise Exception("Organization not found")

        # Derive the service_type based on the role
        service_type = ROLE_TO_SERVICE_TYPE.get(organization["role"].lower())
        # if not service_type:
        #     raise Exception("Service type not found for the given role")

        # Create the new resource
        new_resource = Resource(
            service_type=service_type,
            organization_id=organizationId,
            **input
        )

        db.add(new_resource)
        db.commit()
        db.refresh(new_resource)
        return ResourceOut.from_orm(new_resource)

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

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

@query.field("getMatchingResources")
def resolve_get_matching_resources(_, info, userId, serviceType, location, age=None,
                                   gender=None, languages=None,
                                   costLevel=None, maxDistanceKm=None, limit=5):
    """
    Run your AI‐driven matching logic and return ResourceMatch objects.
    """
    # assemble kwargs for match_resources
    params = {
        "userId": userId,
        "service_type": serviceType,
        "location": location,
        "age": age,
        "gender": gender,
        "languages": languages,
        "cost_level": costLevel,
        "maxDistanceKm": maxDistanceKm,
        "limit": limit,
    }
    matches = match_resources(params, limit)
    db = SessionLocal()
    out = []
    for m in matches:
        r = db.get(Resource, m["resource_id"])
        if not r:
            continue
        out.append({
            "resource": ResourceOut.from_orm(r),
            "score": 1 / (1 + m["distance"]),
        })
    db.close()
    return out

@query.field("requestResourceMatching")
def resolve_request_resource_matching(_, info, **kwargs):
    """
    Alias to getMatchingResources—runs the matching logic and returns the same shape.
    """
    return resolve_get_matching_resources(*args, **kwargs)
    
# ─── Analytics resolvers ─────────────────────────────────────────────────

@query.field("resourcesPerCapita")
def resolve_resources_per_capita(_, info):
    """
    For each (region, category):
      - count resources
      - fetch population_in_need from Region
      - compute per 1,000: (count / population_in_need) * 1000
    """
    db = SessionLocal()

    # 1) count resources grouped by region & service_type
    counts = (
        db.query(
            Resource.region_id,
            Resource.service_type,
            func.count(Resource.resource_id).label("resources_count"),
        )
        .group_by(Resource.region_id, Resource.service_type)
        .all()
    )

    # 2) fetch region metadata in one go
    # regions = {r.resource_id: r for r in db.query(Region).all()}
    regions = {r.region_id: r for r in db.query(Region).all()}


    results = []
    for region_id, category, res_count in counts:
        region = regions.get(region_id)
        pop = region.population_in_need or 1  # avoid div by zero
        per_thousand = (res_count / pop) * 1000
        results.append({
            "regionId": region_id,
            "regionName": region.region_name,
            "category": category,
            "resourcesCount": res_count,
            "populationInNeed": region.population_in_need,
            "perThousandNeeded": round(per_thousand, 2),
        })

    db.close()
    return results

@query.field("resourceNeedGap")
def resolve_resource_need_gap(_, info):
    """
    For each (region, category):
      - demandCount: sum of DemandLog.count
      - supplyCount: number of Resources
      - gap = supplyCount - demandCount
    """
    db = SessionLocal()

    # 1) sum demands
    demand = (
        db.query(
            DemandLog.region_id,
            DemandLog.category,
            func.sum(DemandLog.count).label("demand_count"),
        )
        .group_by(DemandLog.region_id, DemandLog.category)
        .all()
    )

    # 2) reuse resource counts
    supply = (
        db.query(
            Resource.region_id,
            Resource.service_type,
            func.count(Resource.resource_id).label("supply_count"),
        )
        .group_by(Resource.region_id, Resource.service_type)
        .all()
    )

    # index them
    demand_map = {(d.region_id, d.category): d.demand_count for d in demand}
    supply_map = {(s.region_id, s.service_type): s.supply_count for s in supply}

    regions = {r.id: r for r in db.query(Region).all()}

    results = []
    for (region_id, category), demand_count in demand_map.items():
        supply_count = supply_map.get((region_id, category), 0)
        results.append({
            "regionId": region_id,
            "regionName": regions[region_id].name,
            "category": category,
            "demandCount": demand_count,
            "supplyCount": supply_count,
            "gap": supply_count - demand_count,
        })

    db.close()
    return results

@query.field("matchSuccessRate")
def resolve_match_success_rate(_, info, regionId):
    """
    Return a list of (month, successRate) for last 12 months.
    Assuming you log each match attempt and whether it succeeded.
    """
    db = SessionLocal()

    try:
        # Build last 12 month strings
        months = [
            (datetime.date.today().replace(day=1) - datetime.timedelta(days=30 * i))
              .strftime("%Y-%m")
            for i in range(11, -1, -1)
        ]
        # Aggregate on MatchLog.timestamp
        rows = (
            db.query(
                func.to_char(MatchLog.timestamp, 'YYYY-MM').label("month"),
                func.sum(cast(MatchLog.success, Integer)).label("successes"),
                func.count(MatchLog.match_id).label("total"),
            )
            .filter(MatchLog.region_id == regionId)
            .filter(func.to_char(MatchLog.timestamp, 'YYYY-MM').in_(months))
            .group_by("month")
            .order_by("month")
            .all()
        )
        row_map = {r.month: (r.successes, r.total) for r in rows}
        return [
            {
              "month": m,
              "successRate": round((row_map[m][0] / row_map[m][1]) if row_map[m][1] else 0.0, 2)
            }
            for m in months
        ]
    finally:
        db.close()

    
