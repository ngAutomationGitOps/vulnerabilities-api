from app.utilities.postgresql import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends
from app.api.services.agents_services import get_agents_count,get_all_agents_count,get_agent_status_by_dept , get_agent_by_env , get_agent_by_dept, get_agent_info

async def get_all_agents_count_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    count = await get_all_agents_count(db)
    return {"count": count}


async def get_agents_count_handler(origin: str, req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    status = None
    if query_params:
        status = query_params.get("status") 
        status = status.lower()
    origin = origin.lower()
    count = await get_agents_count(db , origin , status)
    return {"count": count}

async def get_agent_status_by_dept_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_agent_status_by_dept(db)
    return {"data": data}

async def get_agent_by_env_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_agent_by_env(db)
    return {"data": data}

async def get_agent_by_dept_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_agent_by_dept(db)
    return {"data": data}

async def get_agent_info_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_agent_info(db)
    return {"data": data}


