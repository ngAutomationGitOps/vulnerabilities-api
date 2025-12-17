
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, select, update, delete, func , literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base
from app import models



class ASMOpenPorts(Base):
    __tablename__ = "asm_open_ports"

    id_asm_open_ports = Column(Integer, primary_key=True, index=True)
    port = Column(Integer)
    status = Column(String)
    scan_time = Column(DateTime)
    id_asm_domain = Column(Integer, ForeignKey("asm_domains.id_asm_domain"))

    asmdomain = relationship("ASMDomains", back_populates="asmopenport", lazy="joined")


   

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
    async def get_one(cls, session: AsyncSession,  asm_open_ports_id: int):
        result = await session.execute(select(cls).where(cls.id_asm_open_ports == asm_open_ports_id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def update_one(cls, session: AsyncSession, asm_open_ports_id: int, update_data: dict):
        await session.execute(
            update(cls).where(cls.id_asm_open_ports == asm_open_ports_id).values(**update_data)
        )
        await session.commit()

    @classmethod
    async def delete_one(cls, session: AsyncSession, asm_open_ports_id: int):
        await session.execute(delete(cls).where(cls.id_asm_open_ports == asm_open_ports_id))
        await session.commit()

    @classmethod
    async def count(cls, session: AsyncSession):
        result = await session.execute(select(func.count(cls.id_asm_open_ports)))
        return result.scalar_one()
    
    @classmethod
    async def port_category_counts(cls, session: AsyncSession):
        result = await session.execute(
            select(cls.port, func.count(cls.port))
            .where(cls.status == True)  # remove if you don’t need this condition
            .group_by(cls.port)
        )
        return result.all()
    
    @classmethod
    async def ports_by_domain(cls, session: AsyncSession):
        result = await session.execute(
            select(cls.id_asm_domain,
            models.ASMDomains.domain_name,        # <-- domain name
            cls.port,
            func.count(cls.port))
            .join(models.ASMDomains, models.ASMDomains.id_asm_domain == cls.id_asm_domain)
            .where(cls.status == True)     # remove if not required
            .group_by(cls.id_asm_domain, models.ASMDomains.domain_name, cls.port)
            .order_by(cls.id_asm_domain, cls.port)
        )
        return result.all()
   