from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from models import Base

DATABASE_URL = "postgresql+asyncpg://postgres:wWD;\kxe;uYgo7{@localhost:5432/taskdb"

# Create a database engine
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session