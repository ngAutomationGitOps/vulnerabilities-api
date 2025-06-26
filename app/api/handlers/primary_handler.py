from app.api.services.primary_services import get_all_agents
from fastapi import Request

async def server_check():
    return {"message": "Server is running"}

def get_agents(req: Request):
    query_params = dict(req.query_params)
    agents = get_all_agents(query_params)
    return {"data": agents}
    