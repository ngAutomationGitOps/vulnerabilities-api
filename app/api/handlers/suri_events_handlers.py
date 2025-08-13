from app.utilities.postgresql import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends
from app.api.services.suri_events_services import  get_suri_events_count,get_so_events_map , get_so_events_by_rule_tag, get_so_events_by_severity_label,get_unique_ip,get_alert_rules,get_ip_info



async def get_suri_events_count_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    severity_label = query_params.get("severity_label")  # Extract severity from query params

    if severity_label:
        if severity_label == "High":
            count = await get_suri_events_count(db, severity_label)
        else:
            raise ValueError(f"Invalid Parameter. Its Should be High.")
    else:
        count = await get_suri_events_count(db, None)

    return {"count": count}

async def get_so_events_map_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_so_events_map(db)
    return {"data": data}

async def get_so_events_by_rule_tag_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_so_events_by_rule_tag(db)
    return {"data": data}

async def get_so_events_by_severity_label_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_so_events_by_severity_label(db)
    return {"data": data}

async def get_unique_ip_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    ip_direction = query_params.get("ip_direction")  # Extract severity from query params
    count = await get_unique_ip(db , ip_direction)
    return {"count": count}

async def get_alert_rules_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_alert_rules(db)
    return {"data": data}

async def get_ip_info_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    data = await get_ip_info(db)
    return {"data": data}