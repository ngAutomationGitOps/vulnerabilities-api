

from sqlalchemy import Column, Integer, String, DateTime, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base


class AgentSo(Base):
    __tablename__ = "agents_so"

    id_agent_so = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    version = Column(String)
    registration_date = Column(DateTime)
    status = Column(String)

    agent = relationship("Agent", back_populates="so", uselist=False)

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
    async def count(cls, session: AsyncSession , status: str | None = None):
        if status:
            result = await session.execute(select(func.count(cls.id_agent_so)).where(cls.status == status))
        else:
            result = await session.execute(select(func.count(cls.id_agent_so)))
        return result.scalar_one()
