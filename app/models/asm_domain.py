
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, select, update, delete, func , literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base
from app import models



class ASMDomains(Base):
    __tablename__ = "asm_domains"

    id_asm_domain = Column(Integer, primary_key=True, index=True)
    mongo_id = Column(String)
    domain_name = Column(String)
    asn = Column(String)
    ip_address = Column(String)
    ip_reputation = Column(Integer)
    location_name = Column(String)
    confidence_score = Column(Integer)
    pulse_count = Column(Integer)
    email = Column(String)
    name_server = Column(String)
    other = Column(String)
    records = Column(String)
    scan_time = Column(DateTime)

    asmopenport = relationship("ASMOpenPorts", back_populates="asmdomain", lazy="joined")
    asmsslinfo = relationship("ASMSslInfo", back_populates="asmdomain", lazy="joined")
    asmtechnologies = relationship("ASMTechnologies", back_populates="asmdomain", lazy="joined")
    asmvulnerabilities = relationship("ASMVulnerabilities", back_populates="asmdomain", lazy="joined")


   

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
    async def get_one(cls, session: AsyncSession, asm_domain_id: int):
        result = await session.execute(select(cls).where(cls.id_asm_domain == asm_domain_id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def update_one(cls, session: AsyncSession, asm_domain_id: int, update_data: dict):
        await session.execute(
            update(cls).where(cls.id_asm_domain == asm_domain_id).values(**update_data)
        )
        await session.commit()

    @classmethod
    async def delete_one(cls, session: AsyncSession, asm_domain_id: int):
        await session.execute(delete(cls).where(cls.id_asm_domain == asm_domain_id))
        await session.commit()

    @classmethod
    async def count(cls, session: AsyncSession):
        result = await session.execute(select(func.count(cls.id_asm_domain)))
        return result.scalar_one()
    
   