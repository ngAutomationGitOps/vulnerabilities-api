# app/models/department.py

from sqlalchemy import Column, Integer, String, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base

class Department(Base):
    __tablename__ = "Department"

    id_department = Column(Integer, primary_key=True, index=True)
    department = Column(String)
    name = Column(String)

    agents = relationship("Agent", back_populates="department")

    @classmethod
    async def insert(cls, session: AsyncSession, data: dict):
        obj = cls(**data)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def count(cls, session: AsyncSession):
        result = await session.execute(select(func.count(cls.id_department)))
        return result.scalar_one()
