from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, select, update, delete, func, cast, Float
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base
from app.models import Agent , Department 
import app.models as models


class Detection(Base):
    __tablename__ = "detection_vuln"

    id_detect_vuln = Column(Integer, primary_key=True, index=True)
    mongo_detection_id = Column(String)
    detected_at = Column(DateTime)
    scan_time = Column(DateTime)
    status = Column(String)
    resolved_at = Column(DateTime)
    id_agent = Column(Integer, ForeignKey("agents.id_agent"))
    id_vuln = Column(Integer, ForeignKey("vulnerability.id_vuln"))

    vulnerability = relationship("Vulnerability", back_populates="detections", lazy="select")
    agent = relationship("Agent", back_populates="detections", lazy="select")


   

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
    async def get_one(cls, session: AsyncSession, detection_id: int):
        result = await session.execute(select(cls).where(cls.id_detect_vuln == detection_id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def update_one(cls, session: AsyncSession, detection_id: int, update_data: dict):
        await session.execute(
            update(cls).where(cls.id_detect_vuln == detection_id).values(**update_data)
        )
        await session.commit()

    @classmethod
    async def delete_one(cls, session: AsyncSession, detection_id: int):
        await session.execute(delete(cls).where(cls.id_detect_vuln == detection_id))
        await session.commit()

    @classmethod
    async def count(cls, session: AsyncSession):
        result = await session.execute(select(func.count(cls.id_detect_vuln)))
        return result.scalar_one()
    
    @classmethod
    async def get_vuln_percentages(cls, session: AsyncSession):
        total_stmt = select(func.count(Detection.id_detect_vuln))
        total_result = await session.execute(total_stmt)
        total = total_result.scalar_one()
        stmt = (
        select(Department.department, func.count(Detection.id_detect_vuln))
        .join(Agent, Agent.id_department == Department.id_department)
        .join(Detection, Detection.id_agent == Agent.id_agent)
        .group_by(Department.department)
    )

        result = await session.execute(stmt)
        return result.all() , total


    
    @classmethod
    async def get_vuln_by_os(cls, session: AsyncSession):
        stmt = (
        select(
            models.Vulnerability.severity,
            models.Vulnerability.os_name,
            func.count(Detection.id_detect_vuln).label("count")
        )
        .join(Detection, Detection.id_vuln == models.Vulnerability.id_vuln)
        .group_by(models.Vulnerability.severity, models.Vulnerability.os_name)
    )
        result = await session.execute(stmt)
        return result.all()
    
    @classmethod
    async def get_vuln_by_dept(cls, session: AsyncSession):
        stmt = (
            select(
                Department.name.label("dept"),
                models.Vulnerability.severity,
                func.count(Detection.id_detect_vuln).label("count")
            )
            .join(Agent, Agent.id_department == Department.id_department)
            .join(Detection, Detection.id_agent == Agent.id_agent)
            .join(models.Vulnerability, models.Vulnerability.id_vuln == Detection.id_vuln)
            .group_by(Department.name, models.Vulnerability.severity)
        )
        result = await session.execute(stmt)
        return result.all()
    
    @classmethod
    async def get_cve_count(cls, session: AsyncSession):
        stmt = (
            select(
                models.Vulnerability.cve_id,
                models.Vulnerability.severity,
                func.count(Detection.id_detect_vuln).label("count")
            )
            .join(Detection, Detection.id_vuln == models.Vulnerability.id_vuln)
            .group_by(models.Vulnerability.cve_id, models.Vulnerability.severity)
            .order_by(func.count(Detection.id_detect_vuln).desc())  # Sorting in SQL
        )
        result = await session.execute(stmt)
        return result.all()