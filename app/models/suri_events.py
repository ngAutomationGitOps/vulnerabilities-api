from sqlalchemy import Column, Integer, String, ForeignKey,DateTime, select, update, delete, func, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.utilities.postgresql import Base
from app.models import Department , Agent , AgentWazuh

class SuriEvents(Base):
    __tablename__ = "suri_events"

    id_event = Column(Integer, primary_key=True, index=True)
    mongo_wazuh_event_id = Column(String)
    elastic_agent_id = Column(String)
    scan_time = Column(DateTime)
    severity_label = Column(String)
    observer_name = Column(String)
    observer_ingress_interface = Column(String)
    log_file_path = Column(String)
    direction = Column(String)
    app_proto = Column(Integer)
    payload_printable = Column(String)
    alert_signature = Column(Integer)
    timestamp = Column(DateTime)
    event_ingested = Column(DateTime)
    community_id = Column(String)
    packet_source = Column(String)
    transport = Column(String)
    decoded_data = Column(String)
    rule_action = Column(String)
    rule_category = Column(String)
    rule_name = Column(String)
    rule_reference = Column(String)
    rule_ruleset = Column(String)
    rule_severity = Column(Integer)
    rule_uuid = Column(String)
    rule_confidence = Column(String)
    rule_updated_at = Column(DateTime)
    source_ip = Column(String)
    source_port = Column(Integer)
    destination_ip = Column(String)
    destination_port = Column(Integer)
    destination_geo_ip = Column(String)
    destination_geo_city_name = Column(String)
    destination_geo_country_name = Column(String)
    destination_asn = Column(String)
    destination_organization_name = Column(String)


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
    async def count(cls, session: AsyncSession, severity_label):
        if severity_label:
            stmt = (
            select(func.count(cls.id_event))
            .where(cls.severity_label == "high")
            )
            result = await session.execute(stmt)
        else:
            result = await session.execute(select(func.count(cls.id_event)))
        return result.scalar_one()
        
    
    
    @classmethod
    async def so_events_map(cls, session: AsyncSession):
        stmt = (
            select(
                cls.destination_geo_country_name,
                func.count(cls.id_event)
            )
            .where(cls.destination_geo_country_name.isnot(None))
            .group_by(cls.destination_geo_country_name)
        )
        result = await session.execute(stmt)
        return result.all()
    
    @classmethod
    async def so_events_by_rule_tag(cls, session: AsyncSession):
        total_stmt = (
            select(func.count(cls.id_event))
        )
        total_result = await session.execute(total_stmt)
        total = total_result.scalar_one()
        stmt = (
            select(
                func.coalesce(
                    func.nullif(cls.rule_category, ""),  # convert empty string to NULL
                    literal("Misc")
                ).label("rule_category"),
                func.count(cls.id_event)
            )
            .group_by("rule_category")
        )
        result = await session.execute(stmt)
        rows = result.all()
        return rows, total
    
    @classmethod
    async def so_events_by_severity_label(cls, session: AsyncSession):
        total_stmt = (
            select(func.count(cls.id_event))
        )
        total_result = await session.execute(total_stmt)
        total = total_result.scalar_one()
        stmt = (
            select(
                cls.severity_label ,
                func.count(cls.id_event)
            )
            .group_by(cls.severity_label)
        )
        result = await session.execute(stmt)
        rows = result.all()
        return rows, total
    
    @classmethod
    async def unique_ip(cls, session: AsyncSession, ip_direction):
        ip_direction = ip_direction.lower()  
        if ip_direction == "source":
            stmt = (
                select(func.count(func.distinct(cls.source_ip)))
                .where(cls.source_ip.isnot(None))
            )
        elif ip_direction == "destination":
            stmt = (
                select(func.count(func.distinct(cls.destination_ip)))
                .where(cls.destination_ip.isnot(None))
            )
        else:
            raise ValueError(f"Invalid ip_direction: {ip_direction}. Must be 'source' or 'destination'.")

        result = await session.execute(stmt)
        return result.scalar_one()