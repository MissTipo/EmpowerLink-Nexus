# user-profile-service/app/graphql/resolvers.py

from app.models import UserProfile
from app.database import SessionLocal
from app.schemas import UserProfileResponse

def resolve_getUserProfile(_, info, id):
    db = SessionLocal()
    try:
        user = db.query(UserProfile).filter(UserProfile.id == int(id)).first()
        if user:
            return UserProfileResponse.model_validate(user).model_dump()
        return None
    finally:
        db.close()

def resolve_createUserProfile(_, info, input):
    db = SessionLocal()
    try:
        new_user = UserProfile(**input)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserProfileResponse.model_validate(new_user).model_dump()
    finally:
        db.close()

def resolve_updateUserProfile(_, info, id, input):
    db = SessionLocal()
    try:
        user = db.query(UserProfile).filter(UserProfile.id == int(id)).first()
        if not user:
            return None
        for key, value in input.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return UserProfileResponse.model_validate(user).model_dump()
    finally:
        db.close()

def resolve_getUserProfileByPhoneNumber(_, info, phone_number):
    db = SessionLocal()
    try:
        user = db.query(UserProfile).filter(UserProfile.phone_number == phone_number).first()
        if user:
            return UserProfileResponse.model_validate(user).model_dump()
        return None
    finally:
        db.close()

def resolve_getUserProfileByName(_, info, name):
    db = SessionLocal()
    try:
        user = db.query(UserProfile).filter(UserProfile.name == name).first()
        if user:
            return UserProfileResponse.model_validate(user).model_dump()
        return None
    finally:
        db.close()

def resolve_updateUserProfileByPhoneNumber(_, info, phone_number, input):
    db = SessionLocal()
    try:
        user = db.query(UserProfile).filter(UserProfile.phone_number == phone_number).first()
        if not user:
            return None
        for key, value in input.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return UserProfileResponse.model_validate(user).model_dump()
    finally:
        db.close()

def resolve_getUsersByLocation(_, info, location):
    db = SessionLocal()
    try:
        users = db.query(UserProfile).filter(UserProfile.location == location).all()
        return [UserProfileResponse.model_validate(u).model_dump() for u in users]
    finally:
        db.close()

# def resolve_allUserProfiles(_, info):
#     db = SessionLocal()
#     try:
#         users = db.query(UserProfile).all()
#         return [UserProfileResponse.model_validate(u).model_dump() for u in users]
#     finally:
#         db.close()
#

def resolve_allUserProfiles(_, info):
    db = SessionLocal()
    try:
        users = db.query(UserProfile).all()
        print("Fetched users from DB:", users)  # Add this
        return [UserProfileResponse.model_validate(u).model_dump() for u in users]
    finally:
        db.close()

