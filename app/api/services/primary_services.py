from sqlalchemy.future import select
from app.models.agents import Agent as AgentModel
from sqlalchemy.ext.asyncio import AsyncSession 
from app.models.fim import Fim
from sqlalchemy.orm import joinedload
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
    stmt = select(Fim).options(joinedload(Fim.agent))
    result = await session.execute(stmt)
    return result.scalars().all()

from app.models.fim import Fim
from app.models.agents import Agent
from app.models.department import Department


async def get_fim_event_percentages_by_department(session: AsyncSession):
    total_stmt = select(func.count(Fim.id_fim))
    total_result = await session.execute(total_stmt)
    total = total_result.scalar_one()

    if total == 0:
        return {}

    # Get count grouped by department name
    stmt = (
        select(Department.department, func.count(Fim.id_fim))
        .join(Agent, Agent.id_department == Department.id_department)
        .join(Fim, Fim.id_agent == Agent.id_agent)
        .group_by(Department.department)
    )

    result = await session.execute(stmt)
    rows = result.all()

    return {
        department_name: round((count / total) * 100, 2)
        for department_name, count in rows
    }