from app.api.services.primary_services import get_all_agents
from fastapi import Request
from app.api.services.primary_services import get_vulnerability_count, get_cve_count, get_server_count , get_status , get_current_username , get_all_cve_summaries
from fastapi import Depends
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html , get_redoc_html


async def get_docs(username: str = Depends(get_current_username)) -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger UI")

async def get_redoc(username: str = Depends(get_current_username)) -> HTMLResponse:
    return get_redoc_html(openapi_url="/openapi.json", title="ReDoc")

async def server_check():
    return {"message": "Server is running"}

async def get_agents(req: Request):
    query_params = dict(req.query_params)
    agents = get_all_agents(query_params)
    return {"data": agents}
    

async def vulnerability_count(req: Request):
    query_params = dict(req.query_params)  
    count = get_vulnerability_count(query_params)
    return {"vulnerability_count": count}

async def cve_count(req: Request):
    query_params = dict(req.query_params)  
    count = get_cve_count(query_params)
    return {"vulnerability_count": count}

async def server_count(req: Request):
    query_params = dict(req.query_params)  
    count = get_server_count(query_params)
    return {"vulnerability_count": count}


async def get_status_vulnerabilities(req: Request):
    query_params = dict(req.query_params) 
    result = get_status(query_params)
    return result

async def get_all_cves(req: Request):
    query_params = dict(req.query_params)
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", 100))

    data = get_all_cve_summaries({}, skip=skip, limit=limit)
    return {"count": len(data), "data": data}


