# app/models/agents.py

from sqlalchemy import Column, Integer, String, ForeignKey, select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base

class Agent(Base):
    __tablename__ = "agents"

    id_agent = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String)
    ip_address = Column(String)
    os_name = Column(String)
    os_platform = Column(String)
    server_environment = Column(String)
    os_version = Column(String)
    id_agent_wazuh = Column(Integer, ForeignKey("agents_wazuh.id_agent_wazuh"))
    id_department = Column(Integer, ForeignKey("department.id_department"))

    wazuh = relationship("AgentWazuh", back_populates="agent", lazy="joined")
    department = relationship("Department", back_populates="agents", lazy="joined")

   

    @classmethod
    async def insert(cls, session: AsyncSession, data: dict):
        obj = cls(**data)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def insert_many(cls, session: AsyncSession, data_list: list[dict]):
        objs = [cls(**data) for data in data_list]
        session.add_all(objs)
        await session.commit()
        return objs

    @classmethod
    async def get_one(cls, session: AsyncSession, agent_id: int):
        result = await session.execute(select(cls).where(cls.id_agent == agent_id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def update_one(cls, session: AsyncSession, agent_id: int, update_data: dict):
        await session.execute(
            update(cls).where(cls.id_agent == agent_id).values(**update_data)
        )
        await session.commit()

    @classmethod
    async def delete_one(cls, session: AsyncSession, agent_id: int):
        await session.execute(delete(cls).where(cls.id_agent == agent_id))
        await session.commit()

    @classmethod
    async def count(cls, session: AsyncSession):
        result = await session.execute(select(func.count(cls.id_agent)))
        return result.scalar_one()
