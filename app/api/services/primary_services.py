from sqlalchemy.future import select
from app.models.agents import Agent as AgentModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.fim import Fim
from sqlalchemy import func

async def get_all_agents_postgres(session: AsyncSession, query: dict = {}):
    result = await session.execute(select(AgentModel))
    agents = result.scalars().all()
    return agents


async def get_fim_count(session: AsyncSession):
    return await Fim.count(session)

async def get_fim_event_counts(cls, session: AsyncSession):
        stmt = select(cls.event, func.count()).group_by(cls.event)
        result = await session.execute(stmt)
        rows = result.all()
        return {event: count for event, count in rows}
    
async def get_fim_event_counts_service(db):
    result = await Fim.get_grouped_event_counts(db)
    rows = result.all()
    return {event: count for event, count in rows}

async def get_fim_events(session: AsyncSession, query: dict = {}):
    stmt = select(Fim)
    result = await session.execute(stmt)
    return result.scalars().all()