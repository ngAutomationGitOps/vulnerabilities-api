from sqlalchemy.future import select
from app.models.agents import Agent as AgentModel
from sqlalchemy.ext.asyncio import AsyncSession 
from app.models import Agent , AgentWazuh , AgentSo

async def get_all_agents_count(session: AsyncSession, query: dict = {}):
    return await Agent.count(session)
    

async def get_agents_count(session: AsyncSession, origin, status, query: dict = {}):
    if origin == "so":
        if status:   
            if status == "active" or status == "disconnected" or status == "decomissioned":
                return await AgentSo.count(session , status)
            else:
                raise ValueError(f"Invalid status: {status}. Must be 'active' , 'disconnected' or 'decomissioned'.")
        else:
            return await AgentSo.count(session)
    elif origin == "wazuh":
        if status:   
            if status == "active" or status == "disconnected" or status == "decomissioned":
                return await AgentWazuh.count(session , status)
            else:
                raise ValueError(f"Invalid status: {status}. Must be 'active' , 'disconnected' or 'decomissioned'.")
        else:
            return await AgentWazuh.count(session)
    else:
        raise ValueError(f"Invalid origin: {origin}. Must be 'so' or 'wazuh'.")
    
async def get_agent_status_by_dept(session: AsyncSession):
    rows = await Agent.agent_status_by_dept(session)
    data = {}
    for dept, status, count in rows:
        data.setdefault(dept, {})[status] = count
    return data

async def get_agent_by_env(session: AsyncSession):
    rows , total = await Agent.agent_by_env(session)
    data = {}
    for env,count in rows:
        data[env] = count
    data["Total"] = total
    return data

