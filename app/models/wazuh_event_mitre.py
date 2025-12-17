from sqlalchemy import Column, Integer, String, ForeignKey,DateTime, select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base


class WazuhEventsMitre(Base):
    __tablename__ = "wazuh_event_mitre"

    id_mitre = Column(Integer, primary_key=True, index=True)
    mitre_id = Column(String)
    mitre_technique = Column(String)
    id_event = Column(Integer, ForeignKey("wazuh_events.id_event"))

    wazuh_event = relationship("WazuhEvents", back_populates="wazuh_events_mitre", lazy="select")


   

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
    async def get_one(cls, session: AsyncSession, mitre_id: int):
        result = await session.execute(select(cls).where(cls.id_mitre == mitre_id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def update_one(cls, session: AsyncSession, mitre_id: int, update_data: dict):
        await session.execute(
            update(cls).where(cls.id_mitre == mitre_id).values(**update_data)
        )
        await session.commit()

    @classmethod
    async def delete_one(cls, session: AsyncSession, mitre_id: int):
        await session.execute(delete(cls).where(cls.id_mitre == mitre_id))
        await session.commit()

    @classmethod
    async def count(cls, session: AsyncSession):
        result = await session.execute(select(func.count(cls.id_mitre)))
        return result.scalar_one()
