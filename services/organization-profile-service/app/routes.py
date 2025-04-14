# app/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import Token
from app.auth import verify_password, create_access_token
from app.models import Organization

router = APIRouter()

@router.post("/signin", response_model=Token)
def signin(email: str, password: str, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.email == email).first()
    if not org or not verify_password(password, org.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token_data = {"sub": org.email, "role": org.role, "org_id": org.id}
    token = create_access_token(data=token_data)
    return {"access_token": token, "token_type": "bearer"}

