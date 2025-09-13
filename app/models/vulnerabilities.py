
from sqlalchemy import Column, Integer,DateTime, String, ForeignKey, select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base
from app.models import Agent, Department, Detection


class Vulnerability(Base):
    __tablename__ = "vulnerability"

    id_vuln = Column(Integer, primary_key=True, index=True)
    mongo_vuln_id = Column(String)
    cve_id = Column(String)
    severity = Column(String)
    description = Column(String)
    reference = Column(String)
    os_name = Column(String)
    os_platform = Column(String)
    os_full = Column(String)
    package_name = Column(String)
    package_verion = Column(String)
    package_type = Column(String)
    remediation = Column(String)
    detected_at = Column(DateTime)
    scan_time = Column(DateTime)

    detections = relationship("Detection", back_populates="vulnerability")


   

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
    async def get_one(cls, session: AsyncSession, vuln_id: int):
        result = await session.execute(select(cls).where(cls.id_vuln == vuln_id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def update_one(cls, session: AsyncSession, vuln_id: int, update_data: dict):
        await session.execute(
            update(cls).where(cls.id_vuln == vuln_id).values(**update_data)
        )
        await session.commit()

    @classmethod
    async def delete_one(cls, session: AsyncSession, vuln_id: int):
        await session.execute(delete(cls).where(cls.id_vuln == vuln_id))
        await session.commit()

    @classmethod
    async def count(cls, session: AsyncSession):
        result = await session.execute(select(func.count(cls.id_vuln)))
        return result.scalar_one()

    @classmethod
    async def count_vulnerabilities_by_severity(cls, session, severity_status: str) -> int:
        stmt = (
            select(func.count(Detection.id_detect_vuln))
            .join(Vulnerability, Detection.id_vuln == Vulnerability.id_vuln)
            .where(Vulnerability.severity == severity_status)
        )

        result = await session.execute(stmt)
        return result.scalar_one()


    @classmethod
    async def vuln_desc(cls, session):
        stmt = (
            select(Vulnerability.cve_id, Vulnerability.description, Vulnerability.remediation)
        )

        result = await session.execute(stmt)
        return result.all()
    


