# app/graphql/resolvers.py
import httpx
from sqlalchemy.orm import Session
from app.models import Organization
from app.database import SessionLocal
from app.schemas import OrganizationCreate
from app.auth import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from config.settings import settings

# Helper: get a new DB session
def get_db_session() -> Session:
    return SessionLocal()

# Resolver for signup
def resolve_signupOrganization(_, info, input):
    db: Session = get_db_session()
    # Check if email already exists
    existing = db.query(Organization).filter(Organization.email == input["email"]).first()
    if existing:
        return None  # Optionally return an error message, or raise an exception.
    hashed_password = get_password_hash(input["password"])
    new_org = Organization(
        name=input["name"],
        email=input["email"],
        phone=input.get("phone"),
        location=input.get("location"),
        role=input.get("role", "Organization"),
        password=hashed_password
    )
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    db.close()
    return new_org

# Resolver for signin
def resolve_signinOrganization(_, info, email, password):
    db: Session = get_db_session()
    org = db.query(Organization).filter(Organization.email == email).first()
    db.close()
    if not org or not verify_password(password, org.password):
        return None  # Optionally return an error; GraphQL errors could be raised.
    token_data = {
        "sub": org.email,
        "role": org.role,
        "org_id": org.id
    }
    access_token = create_access_token(data=token_data, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

# Resolver for updating an organization profile
def resolve_updateOrganizationProfile(_, info, id, input):
    db: Session = get_db_session()
    org = db.query(Organization).filter(Organization.id == int(id)).first()
    if not org:
        return None
    for key, value in input.items():
        if value is not None:
            setattr(org, key, value)
    db.commit()
    db.refresh(org)
    db.close()
    return org

# Resolver for querying a single organization
def resolve_getOrganization(_, info, id):
    db: Session = get_db_session()
    org = db.query(Organization).filter(Organization.id == int(id)).first()
    db.close()
    return org

# Resolver for listing organizations by location and role
def resolve_listOrganizations(_, info, location=None, role=None):
    db: Session = get_db_session()
    query = db.query(Organization)
    if location:
        query = query.filter(Organization.location == location)
    if role:
        query = query.filter(Organization.role == role)
    orgs = query.all()
    db.close()
    return orgs

