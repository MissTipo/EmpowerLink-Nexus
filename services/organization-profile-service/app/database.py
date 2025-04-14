# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use the recommended declarative base method from sqlalchemy.orm
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# Dependency for FastAPI routes/resolvers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

