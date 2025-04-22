from app.database import Base, engine
from app.models import Resource

Base.metadata.create_all(bind=engine)
print("✅ Database tables created.")

