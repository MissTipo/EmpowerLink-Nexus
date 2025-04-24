import json
from ariadne import QueryType
from sqlalchemy import func

from app.database import get_db
from app.models import ResourceLocation

query = QueryType()

import logging
logger = logging.getLogger("geospatial")
@query.field("serviceDeserts")
def resolve_service_deserts(_, info, radiusKm):
    logger.info(f"serviceDeserts called with radiusKm={radiusKm}")
    ...

def resolve_all_locations(_, info):
    db = next(get_db())
    rows = db.query(ResourceLocation).all()
    features = []
    for r in rows:
        geom_json = db.scalar(func.ST_AsGeoJSON(r.location))
        features.append({
            "type": "Feature",
            "geometry": json.loads(geom_json),
            "properties": {
                "resource_id": r.resource_id,
                "service_type": r.service_type,
            },
        })
    return {"type": "FeatureCollection", "features": features}

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    φ1, φ2 = radians(lat1), radians(lat2)
    Δφ = radians(lat2 - lat1)
    Δλ = radians(lon2 - lon1)
    a = sin(Δφ/2)**2 + cos(φ1)*cos(φ2)*sin(Δλ/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def resolve_service_deserts(_, info, radiusKm):
    db = next(get_db())
    # 1) Get bounding box of all points
    extent = db.scalar(func.ST_Extent(ResourceLocation.location))

    # 2) No rows → immediate empty
    if not extent:
        return {"type": "FeatureCollection", "features": []}

    # 3) Parse BOX(lon1 lat1,lon2 lat2)
    box = extent.replace("BOX(", "").replace(")", "").split(",")
    lon1, lat1 = map(float, box[0].split())
    lon2, lat2 = map(float, box[1].split())

    # 4) If radius covers the whole diagonal, no deserts
    diagonal = haversine_km(lat1, lon1, lat2, lon2)
    if radiusKm >= diagonal:
        return {"type": "FeatureCollection", "features": []}

    nx, ny = 10, 10
    dx, dy = (lon2 - lon1)/nx, (lat2 - lat1)/ny

    deserts = []
    for i in range(nx):
        for j in range(ny):
            cell = func.ST_MakeEnvelope(
                lon1 + i*dx, lat1 + j*dy,
                lon1 + (i+1)*dx, lat1 + (j+1)*dy,
                4326
            )
            centroid = func.ST_Centroid(cell)
            found = (
                db.query(ResourceLocation)
                  .filter(func.ST_DWithin(
                      ResourceLocation.location,
                      centroid,
                      radiusKm * 1000
                  ))
                  .first()
            )
            if not found:
                poly_json = db.scalar(func.ST_AsGeoJSON(cell))
                deserts.append({
                    "type": "Feature",
                    "geometry": json.loads(poly_json),
                    "properties": {}
                })
    return {"type": "FeatureCollection", "features": deserts}

