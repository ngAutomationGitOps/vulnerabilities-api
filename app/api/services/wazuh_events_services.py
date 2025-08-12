from sqlalchemy.future import select
from app.models.agents import Agent as AgentModel
from sqlalchemy.ext.asyncio import AsyncSession 
from app.models.fim import Fim
from sqlalchemy.orm import joinedload
from sqlalchemy import func 
from app.models import WazuhEvents , WazuhEventsRuleGroup, WazuhEventsMitre

async def get_wazuh_events_count(session: AsyncSession):
    return await WazuhEvents.count(session)

async def get_user_count(session: AsyncSession):
    return await WazuhEvents.users_count(session)

async def get_event_by_user(session: AsyncSession):
    rows = await WazuhEvents.events_by_user(session)
    return [
        { target_user : events_count }
        for target_user , events_count in rows
    ]
    
async def get_event_by_srcip(session: AsyncSession):
    rows = await WazuhEvents.events_by_srcip(session)
    return [
        { srcip : events_count }
        for srcip , events_count in rows
    ]
    
async def get_event_by_status(session: AsyncSession):
    rows,total = await WazuhEvents.events_by_status(session)
    result = [{"total": total}]
    result.extend({status: events_count} for status, events_count in rows)
    return result
    
async def get_event_by_dept(session: AsyncSession):
    rows , total = await WazuhEvents.events_by_dept(session)
    result = [{"total": total}]
    result.extend({dept: events_count} for dept, events_count in rows)
    return result

async def get_event_map(session: AsyncSession):
    rows = await WazuhEvents.events_map(session)
    return [
        { srcCountry : events_count }
        for srcCountry, events_count in rows
    ]