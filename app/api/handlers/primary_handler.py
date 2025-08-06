from app.api.services.primary_services import get_all_agents_postgres
from app.utilities.postgresql import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends


async def get_agents(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    agents = await get_all_agents_postgres(db, query_params)
    return {"data": [agent.__dict__ for agent in agents]}
