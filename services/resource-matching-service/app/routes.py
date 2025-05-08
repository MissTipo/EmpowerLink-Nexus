from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.schemas import MatchRequest, ResourceMatch
from ai.matching_model import match_resources
from app.database import SessionLocal
from app.models import Resource
from typing import List

router = APIRouter()

@router.post("/match", response_model=List[ResourceMatch])
def get_matching_resources(request: MatchRequest):
    try:
        # 1. Run AI-based matching logic (returns list of dicts with resource_id + distance)
        matched_ids_with_scores = match_resources(request.dict())

        resource_ids = [item["resource_id"] for item in matched_ids_with_scores]

        # 2. Fetch resource details from DB
        db: Session = SessionLocal()
        matched_resources = db.query(Resource).filter(Resource.resource_id.in_(resource_ids)).all()
        db.close()

        # 3. Reorder & structure response
        resource_map = {str(r.resource_id): r for r in matched_resources}
        ordered_results = []
        for match in matched_ids_with_scores:
            res_obj = resource_map.get(match["resource_id"])
            if res_obj:
                resource_out = {
                    "resource_id": str(res_obj.id),
                    "service_type": res_obj.service_type,
                    "latitude": res_obj.latitude,
                    "longitude": res_obj.longitude,
                    "cost_level": res_obj.cost_level,
                    "languages_supported": res_obj.languages_supported,
                    "capacity": res_obj.capacity,
                    "tags": res_obj.tags,
                }
                score = round(1 / (match["distance"] + 1e-5), 4)  # Inverse distance as score
                ordered_results.append({"resource": resource_out, "score": score})

        return ordered_results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

