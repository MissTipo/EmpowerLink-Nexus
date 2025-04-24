import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ResourceLocation

router = APIRouter()

@router.get("/resources", summary="All resources as GeoJSON")
def list_resources(db: Session = Depends(get_db)):
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

@router.get("/service-deserts", summary="Cells with no nearby resources")
def find_service_deserts(
    radius_km: float = Query(5.0, description="Radius in kilometers"),
    db: Session = Depends(get_db),
):
    # compute bounding box of all points
    extent = db.query(func.ST_Extent(ResourceLocation.location)).scalar()
    if not extent:
        return {"type": "FeatureCollection", "features": []}
        # raise HTTPException(status_code=404, detail="No resources found")
    # parse BOX(lon1 lat1,lon2 lat2)
    box = extent.replace("BOX(", "").replace(")", "").split(",")
    lon1, lat1 = map(float, box[0].split())
    lon2, lat2 = map(float, box[1].split())

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
                      radius_km * 1000
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

