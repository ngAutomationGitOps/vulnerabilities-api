
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, case, or_, select, update, delete, func , literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base
from app import models



class ASMVulnerabilities(Base):
    __tablename__ = "asm_vulnerabilities"

    id_asm_vulnerabilities = Column(Integer, primary_key=True, index=True)
    vul_name = Column(String)
    severity = Column(String)
    cve_id = Column(String)
    cwe_ids = Column(String)
    tags = Column(String)
    url = Column(String)
    vul_path = Column(String)
    matched_at = Column(String)
    extracted_results = Column(String)
    status = Column(String)
    scan_time = Column(DateTime)
    id_asm_domain = Column(Integer, ForeignKey("asm_domains.id_asm_domain"))
    

    asmdomain = relationship("ASMDomains", back_populates="asmvulnerabilities", lazy="joined")


   

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
    async def get_one(cls, session: AsyncSession, asm_vulnerabilities_id: int):
        result = await session.execute(select(cls).where(cls.id_asm_vulnerabilities == asm_vulnerabilities_id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def update_one(cls, session: AsyncSession, asm_vulnerabilities_id: int, update_data: dict):
        await session.execute(
            update(cls).where(cls.id_asm_vulnerabilities == asm_vulnerabilities_id).values(**update_data)
        )
        await session.commit()

    @classmethod
    async def delete_one(cls, session: AsyncSession, asm_vulnerabilities_id: int):
        await session.execute(delete(cls).where(cls.id_asm_vulnerabilities == asm_vulnerabilities_id))
        await session.commit()

    @classmethod
    async def count(cls, session: AsyncSession):
        result = await session.execute(select(func.count(cls.id_asm_vulnerabilities)))
        return result.scalar_one()
    
    @classmethod
    async def critical_severities_count(cls, session: AsyncSession):
        result = await session.execute(
            select(func.count(cls.id_asm_vulnerabilities)).where(
                cls.severity == "critical"
            )
        )
        return result.scalar_one()
    
    @classmethod
    async def vulnerabilities_by_severity(cls, session: AsyncSession):
        result = await session.execute(
            select(
                cls.severity, 
                func.count(cls.id_asm_vulnerabilities))
            .where(cls.severity != "critical")
            .group_by(cls.severity)
        )
        return result.all()
    
    @classmethod
    async def top_vulnerabilities(cls, session: AsyncSession):
        severity_order = case(
            (cls.severity == "critical", 1),
            (cls.severity == "high", 2),
            else_=3
        )

        result = await session.execute(
            select(
                cls.id_asm_domain,
                models.ASMDomains.domain_name,
                models.ASMDomains.ip_address,
                cls.severity,
                cls.vul_name
            )
            .join(
                models.ASMDomains,
                models.ASMDomains.id_asm_domain == cls.id_asm_domain
            )
            .where(or_(cls.severity == "info", cls.severity == "high"))
            .order_by(severity_order, models.ASMDomains.domain_name)
        )

        return result.all()