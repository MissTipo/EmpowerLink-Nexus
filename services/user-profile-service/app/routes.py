# user-profile-service/app/routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import UserProfileCreate, UserProfileResponse, UserProfileUpdate
from app import models
# from config.settings import get_db
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=UserProfileResponse)
def create_user_profile(profile: UserProfileCreate, db: Session = Depends(get_db)):
    # For now, a simple in-memory placeholder (later use SQLAlchemy session)
    db_user = models.UserProfile(**profile.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserProfileResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserProfileResponse)
def update_user_profile(user_id: int, profile: UserProfileUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in profile.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

