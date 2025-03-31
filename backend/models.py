from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

    @classmethod
    async def get_all(cls, db: AsyncSession):
        result = await db.execute(select(cls))
        return result.scalars().all()