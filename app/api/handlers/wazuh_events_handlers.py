from app.utilities.postgresql import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends
from app.api.services.wazuh_events_services import get_wazuh_events_count , get_user_count , get_event_by_user, get_event_by_srcip, get_event_by_status, get_event_by_dept, get_events_map, get_impacted_servers, get_recent_events

async def get_wazuh_events_count_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    count = await get_wazuh_events_count(db)
    return {"count": count}

async def get_user_count_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    count = await get_user_count(db)
    return {"count": count}

async def get_events_by_user_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_event_by_user(db)
    return {"data": data}

async def get_events_by_srcip_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_event_by_srcip(db)
    return {"data": data}

async def get_events_by_status_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_event_by_status(db)
    return {"data": data}

async def get_events_by_dept_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_event_by_dept(db)
    return {"data": data}

async def get_events_map_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_events_map(db)
    return {"data": data}

async def get_impacted_servers_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_impacted_servers(db)
    return {"data": data}

async def get_recent_events_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_recent_events(db)
    return {"data": data}