# app/models/agents.py

from sqlalchemy import Column, Integer, String, ForeignKey, select, update, delete, func , literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base
from app import models



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
    id_agent_so = Column(Integer, ForeignKey("agents_so.id_agent_so"))
    id_client = Column(Integer, ForeignKey("client.id_client"))

    wazuh = relationship("AgentWazuh", back_populates="agent", lazy="joined")
    so = relationship("AgentSo", back_populates="agent", lazy="joined")
    client = relationship("Client", back_populates="agent", lazy="joined")
    department = relationship("Department", back_populates="agents", lazy="joined")
    fim = relationship("Fim", back_populates="agent", lazy="select")
    detections = relationship("Detection", back_populates="agent", lazy="select")


   

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
    
    @classmethod
    async def agent_status_by_dept(cls, session: AsyncSession):
        stmt = (
        select(func.coalesce(
                    func.nullif(cls.server_environment, ""),  # convert empty string to NULL
                    literal("Others")
                ).label("server_environment")
               , models.AgentWazuh.status
               , func.count(Agent.id_agent))
        .join(models.AgentWazuh, models.AgentWazuh.id_agent_wazuh == cls.id_agent_wazuh)
        .group_by(cls.server_environment)
        .group_by(models.AgentWazuh.status)
    )

        result = await session.execute(stmt)
        return result.all()
    
    @classmethod
    async def agent_by_env(cls, session: AsyncSession):
        total_stmt = select(func.count(cls.id_agent))
        total_result = await session.execute(total_stmt)
        total = total_result.scalar_one()
        stmt = (
        select(func.coalesce(
                    func.nullif(cls.server_environment, ""),  # convert empty string to NULL
                    literal("Others")
                ).label("server_environment")
               , func.count(Agent.id_agent))
        .group_by(cls.server_environment)
    )

        result = await session.execute(stmt)
        return result.all() , total
