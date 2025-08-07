# app/models/fim.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base


class Fim(Base):
    __tablename__ = "fim"

    id_fim = Column(Integer, primary_key=True, index=True)
    id_agent = Column(Integer, ForeignKey("agents.id_agent"))
    rule_id = Column(String)
    severity = Column(String)
    description = Column(String)
    event = Column(String)
    path = Column(String)
    detected_at = Column(DateTime)
    scan_time = Column(DateTime)

    agent = relationship("Agent", back_populates="fim", lazy="joined")

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
    async def get_one(cls, session: AsyncSession, fim_id: int):
        result = await session.execute(select(cls).where(cls.id_fim == fim_id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def update_one(cls, session: AsyncSession, fim_id: int, update_data: dict):
        await session.execute(
            update(cls).where(cls.id_fim == fim_id).values(**update_data)
        )
        await session.commit()

    @classmethod
    async def delete_one(cls, session: AsyncSession, fim_id: int):
        await session.execute(delete(cls).where(cls.id_fim == fim_id))
        await session.commit()

    @classmethod
    async def count(cls, session: AsyncSession):
        result = await session.execute(select(func.count(cls.id_fim)))
        return result.scalar_one()

    @classmethod
    async def get_grouped_event_counts(cls, session: AsyncSession):
        stmt = select(cls.event, func.count()).group_by(cls.event)
        return await session.execute(stmt)