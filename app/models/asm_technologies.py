
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, select, update, delete, func , literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base
from app import models



class ASMTechnologies(Base):
    __tablename__ = "asm_technologies"

    id_asm_technologies = Column(Integer, primary_key=True, index=True)
    software = Column(String)
    technologies_version = Column(String)
    is_outdated = Column(Boolean)
    latest_version = Column(String)
    known_plugin = Column(Boolean)
    scan_time = Column(DateTime)
    id_asm_domain = Column(Integer, ForeignKey("asm_domains.id_asm_domain"))
    

    asmdomain = relationship("ASMDomains", back_populates="asmtechnologies", lazy="joined")


   

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
    async def get_one(cls, session: AsyncSession, asm_technologies_id: int):
        result = await session.execute(select(cls).where(cls.id_asm_technologies == asm_technologies_id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def update_one(cls, session: AsyncSession, asm_technologies_id: int, update_data: dict):
        await session.execute(
            update(cls).where(cls.id_asm_technologies == asm_technologies_id).values(**update_data)
        )
        await session.commit()

    @classmethod
    async def delete_one(cls, session: AsyncSession, asm_technologies_id: int):
        await session.execute(delete(cls).where(cls.id_asm_technologies == asm_technologies_id))
        await session.commit()

    @classmethod
    async def count(cls, session: AsyncSession):
        result = await session.execute(select(func.count(cls.id_asm_technologies)))
        return result.scalar_one()
    
    @classmethod
    async def outdated_tech(cls, session: AsyncSession):
        result = await session.execute(
            select(func.count(cls.id_asm_technologies)).where(
                  cls.is_outdated == True      
            )
        )
        return result.scalar_one()
    
   