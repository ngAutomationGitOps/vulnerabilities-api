from fastapi import Request
from fastapi.responses import JSONResponse
from app.api.services.stats_service import get_severity_stats_by_os , get_os_stats_by_severity

async def get_os_grouped_summary(request: Request):
    query_params = dict(request.query_params)
    return get_severity_stats_by_os(query_params)

async def get_severity_grouped_summary(request=None):
    try:
        data = get_os_stats_by_severity()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})