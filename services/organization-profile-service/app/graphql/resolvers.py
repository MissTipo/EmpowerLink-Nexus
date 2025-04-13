from app.models import Organization
from app.database import SessionLocal
from app.schemas import OrganizationResponse
from app.auth.jwt import create_access_token, decode_access_token

def resolve_getOrganizationByEmail(_, info, email):
    db = SessionLocal()
    try:
        org = db.query(Organization).filter(Organization.email == email).first()
        if org:
            return OrganizationResponse.from_orm(org)
        return None
    finally:
        db.close()

def resolve_registerOrganization(_, info, input):
    db = SessionLocal()
    try:
        # Here, you would typically hash the password before saving it.
        new_org = Organization(**input)
        db.add(new_org)
        db.commit()
        db.refresh(new_org)
        return OrganizationResponse.from_orm(new_org)
    finally:
        db.close()

def resolve_loginOrganization(_, info, input):
    db = SessionLocal()
    try:
        org = db.query(Organization).filter(Organization.email == input["email"]).first()
        # In practice, use proper password hashing and verification here.
        if org and org.password == input["password"]:
            token = create_access_token({"sub": org.email})
            return {"access_token": token, "token_type": "bearer"}
        raise Exception("Invalid credentials")
    finally:
        db.close()

def resolve_verifyOrganizationToken(_, info, token):
    payload = decode_access_token(token)
    if payload and "sub" in payload:
        return {"email": payload["sub"]}
    return None

