
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, case, or_, select, update, delete, func , literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base
from app import models



class OSEOLInfo(Base):
    __tablename__ = "os_eol_info"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    name = Column(String)
    version = Column(String)
    end_of_life = Column(DateTime)
    extended_support_end_date = Column(DateTime)
    link = Column(String)
    

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
    async def get_one(cls, session: AsyncSession, eol_id: int):
        result = await session.execute(select(cls).where(cls.id == eol_id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def update_one(cls, session: AsyncSession, eol_id: int, update_data: dict):
        await session.execute(
            update(cls).where(cls.id == eol_id).values(**update_data)
        )
        await session.commit()

    @classmethod
    async def delete_one(cls, session: AsyncSession, eol_id: int):
        await session.execute(delete(cls).where(cls.id == eol_id))
        await session.commit()

    @classmethod
    async def count(cls, session: AsyncSession):
        result = await session.execute(select(func.count(cls.id)))
        return result.scalar_one()
    
