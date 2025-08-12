from sqlalchemy import Column, Integer, String, ForeignKey,DateTime, select, update, delete, func, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base
from app.models import Department , Agent

class WazuhEvents(Base):
    __tablename__ = "wazuh_events"

    id_event = Column(Integer, primary_key=True, index=True)
    mongo_wazuh_event_id = Column(String)
    scan_time = Column(DateTime)
    auth_protocol = Column(String)
    workstation_name = Column(String)
    sub_status = Column(String)
    target_user = Column(String)
    failure_reason = Column(String)
    logon_type = Column(Integer)
    status_code = Column(String)
    event_id = Column(Integer)
    event_time = Column(DateTime)
    source_ip = Column(String)
    source_city = Column(String)
    source_country = Column(String)
    alert_description = Column(String)
    id_agent = Column(Integer, ForeignKey("agents.id_agent"))

    wazuh_events_rule_group = relationship("WazuhEventsRuleGroup", back_populates="wazuh_event", lazy="select")
    wazuh_events_mitre = relationship("WazuhEventsMitre", back_populates="wazuh_event", lazy="select")


   

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
    async def get_one(cls, session: AsyncSession, event_id: int):
        result = await session.execute(select(cls).where(cls.id_event == event_id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def update_one(cls, session: AsyncSession, event_id: int, update_data: dict):
        await session.execute(
            update(cls).where(cls.id_event == event_id).values(**update_data)
        )
        await session.commit()

    @classmethod
    async def delete_one(cls, session: AsyncSession, event_id: int):
        await session.execute(delete(cls).where(cls.id_event == event_id))
        await session.commit()

    @classmethod
    async def count(cls, session: AsyncSession):
        result = await session.execute(select(func.count(cls.id_event)))
        return result.scalar_one()
    
    @classmethod
    async def users_count(cls, session: AsyncSession):
        stmt = select(func.count(func.distinct(cls.target_user))).where(cls.target_user.isnot(None))
        result = await session.execute(stmt)
        return result.scalar_one()
    
    @classmethod
    async def events_by_user(cls, session: AsyncSession):
        stmt = (
            select(
                cls.target_user,
                func.count(cls.id_event)
            )
            .where(cls.target_user.isnot(None))
            .group_by(cls.target_user)
        )
        result = await session.execute(stmt)
        return result.all()

    @classmethod
    async def events_by_srcip(cls, session: AsyncSession):
        stmt = (
            select(
                cls.source_ip,
                func.count(cls.id_event)
            )
            .where(cls.source_ip.isnot(None))
            .group_by(cls.source_ip)
        )
        result = await session.execute(stmt)
        return result.all() 
    
    @classmethod
    async def events_by_status(cls, session: AsyncSession):
        total_stmt = (
    select(func.count(cls.id_event)).where(cls.status_code.isnot(None))
    .join(Agent, cls.id_agent == Agent.id_agent)
)
        total_result = await session.execute(total_stmt)
        total = total_result.scalar_one()
        stmt = (
            select(
                cls.status_code,
                func.count(cls.id_event)
            )
            .where(cls.status_code.isnot(None))
            .group_by(cls.status_code)
        )
        result = await session.execute(stmt)
        return result.all() , total
    
    @classmethod
    async def events_by_dept(cls, session: AsyncSession):
        total_stmt = (
            select(func.count(cls.id_event))
            .join(Agent, cls.id_agent == Agent.id_agent)
        )
        total_result = await session.execute(total_stmt)
        total = total_result.scalar_one()
        stmt = (
            select(
                func.coalesce(Department.department, literal("Unknown")).label("department"),
                func.count(cls.id_event)
            )
            .select_from(cls)
            .join(Agent, cls.id_agent == Agent.id_agent)
            .join(Department, Agent.id_department == Department.id_department, isouter=True)
            .group_by("department")
        )
        result = await session.execute(stmt)
        rows = result.all()
        return rows, total

    @classmethod
    async def events_map(cls, session: AsyncSession):
        stmt = (
            select(
                cls.source_country,
                func.count(cls.id_event)
            )
            .where(cls.source_country.isnot(None))
            .group_by(cls.source_country)
        )
        result = await session.execute(stmt)
        return result.all()
