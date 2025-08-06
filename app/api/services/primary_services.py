from sqlalchemy.future import select
from app.models.agents import Agent as AgentModel
from sqlalchemy.ext.asyncio import AsyncSession

async def get_all_agents_postgres(session: AsyncSession, query: dict = {}):
    result = await session.execute(select(AgentModel))
    agents = result.scalars().all()
    return agents
