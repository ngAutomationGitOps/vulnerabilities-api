from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.orm import joinedload
from sqlalchemy import func 
from app.models import SuriEvents



async def get_suri_events_count(session: AsyncSession, severity_label):
    if severity_label:
        return await SuriEvents.count(session , severity_label)
    else:
        return await SuriEvents.count(session, None)

async def get_so_events_map(session: AsyncSession):
    rows = await SuriEvents.so_events_map(session)
    return [
        { DestCountry : events_count }
        for DestCountry, events_count in rows
    ]

async def get_so_events_by_rule_tag(session: AsyncSession):
    rows , total = await SuriEvents.so_events_by_rule_tag(session)
    if total == 0:
        return {}
    return {
        rule_tag: round((count / total) * 100, 2)
        for rule_tag, count in rows
    }
    
async def get_so_events_by_severity_label(session: AsyncSession):
    rows , total = await SuriEvents.so_events_by_severity_label(session)
    if total == 0:
        return {}
    return {
        severity_label: round((count / total) * 100, 2)
        for severity_label, count in rows
    }
    
async def get_unique_ip(session: AsyncSession, ip_direction):
        return await SuriEvents.unique_ip(session , ip_direction)