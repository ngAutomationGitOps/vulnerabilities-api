from app.api.services.primary_services import get_all_agents_postgres
from app.utilities.postgresql import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends
from app.api.services.primary_services import get_fim_count , get_fim_event_counts_service , get_fim_events , get_fim_event_percentages_by_department, get_vulnerability_count_by_severity, get_vuln_count, get_vuln_percentages_by_department,get_vuln_by_os


async def get_agents(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    agents = await get_all_agents_postgres(db, query_params)
    return {"data": [agent.__dict__ for agent in agents]}


async def get_fim_count_handler(db: AsyncSession = Depends(get_db)):
    count = await get_fim_count(db)
    return {"count": count}

async def get_fim_eventsCount_handler(db: AsyncSession = Depends(get_db)):
    counts = await get_fim_event_counts_service(db)
    return {"counts": counts}

async def get_fim_events_handler(req: Request, db: AsyncSession = Depends(get_db)):
    fim_events = await get_fim_events(db)
    return {"data": fim_events}



async def get_fim_event_percent_by_department_handler(db: AsyncSession = Depends(get_db)):
    data = await get_fim_event_percentages_by_department(db)
    return {"percentages": data}

async def get_vulnerability_count_handler(severity_id: int, session: AsyncSession = Depends(get_db)):
    count = await get_vulnerability_count_by_severity(session, severity_id)
    return {"severity_id": severity_id, "count": count}

async def get_vuln_count_handler(db: AsyncSession = Depends(get_db)):
    count = await get_vuln_count(db)
    return {"count": count}

async def get_vuln_percent_by_department_handler(db: AsyncSession = Depends(get_db)):
    data = await get_vuln_percentages_by_department(db)
    return {"percentages": data}

async def get_vuln_by_os_handler(db: AsyncSession = Depends(get_db)):
    data = await get_vuln_by_os(db)
    return {"data": data}