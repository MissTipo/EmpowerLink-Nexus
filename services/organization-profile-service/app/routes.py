from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import OrganizationCreate, OrganizationResponse, OrganizationLogin
from app.database import get_db
from app.models import Organization

router = APIRouter()

@router.post("/organizations/", response_model=OrganizationResponse)
def create_organization(organization: OrganizationCreate, db: Session = Depends(get_db)):
    db_org = Organization(name=organization.name, email=organization.email, password=organization.password, role=organization.role)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

@router.post("/auth/login", response_model=dict)
def login_organization(org: OrganizationLogin, db: Session = Depends(get_db)):
    # This is a simplified version; use proper error handling and hashing in practice.
    db_org = db.query(Organization).filter(Organization.email == org.email).first()
    if db_org and db_org.password == org.password:
        from app.auth.jwt import create_access_token
        token = create_access_token({"sub": db_org.email})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

