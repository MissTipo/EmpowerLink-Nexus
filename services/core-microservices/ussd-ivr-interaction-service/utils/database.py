from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Update with your actual PostgreSQL connection details
DATABASE_URL = "postgresql+asyncpg://your_username:your_password@localhost/your_db_name"

# Create asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an asynchronous session maker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

