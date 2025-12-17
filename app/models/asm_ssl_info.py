
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, select, update, delete, func , literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base
from app import models



class ASMSslInfo(Base):
    __tablename__ = "asm_ssl_info"

    id_asm_ssl_info = Column(Integer, primary_key=True, index=True)
    ssl_trusted = Column(Boolean)
    ssl_generated = Column(Boolean)
    expired = Column(Boolean)
    valid_till = Column(DateTime)
    is_wildcard = Column(Boolean)
    tls_versions = Column(String)
    ssl_error = Column(String)
    scan_time = Column(DateTime)
    id_asm_domain = Column(Integer, ForeignKey("asm_domains.id_asm_domain"))
    

    asmdomain = relationship("ASMDomains", back_populates="asmsslinfo", lazy="joined")


   

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
    async def get_one(cls, session: AsyncSession, asm_ssl_info_id: int):
        result = await session.execute(select(cls).where(cls.id_asm_ssl_info == asm_ssl_info_id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def update_one(cls, session: AsyncSession, asm_ssl_info_id: int, update_data: dict):
        await session.execute(
            update(cls).where(cls.id_asm_ssl_info == asm_ssl_info_id).values(**update_data)
        )
        await session.commit()

    @classmethod
    async def delete_one(cls, session: AsyncSession, asm_ssl_info_id: int):
        await session.execute(delete(cls).where(cls.id_asm_ssl_info == asm_ssl_info_id))
        await session.commit()

    @classmethod
    async def count(cls, session: AsyncSession):
        result = await session.execute(select(func.count(cls.id_asm_ssl_info)))
        return result.scalar_one()
    
    @classmethod
    async def issues_count(cls, session: AsyncSession):
        result = await session.execute(
            select(func.count(cls.id_asm_ssl_info)).where(
                cls.ssl_error.isnot(None),
                cls.ssl_error != "timed out"
            )
        )
        return result.scalar_one()
   