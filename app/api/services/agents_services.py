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

async def get_agent_by_dept(session: AsyncSession):
    rows , total = await Agent.agent_by_dept(session)
    data = {}
    for dept,count in rows:
        data[dept] = count
    data["Total"] = total
    return data


async def get_agent_info(session: AsyncSession):
    rows = await Agent.agent_info(session)
    return [
            {
                "Agent ID" : agent_id,
                "Server_Environment" : server_environment,
                "Agent_Name" : agent_name,
                "Ip_Address" : ip_address,
                "Server_Owner" : server_owner,
                "client_name" : client_name,
                "cs_owner" : cs_owner,
                "wazuh_status" : wazuh_status,
                "end_of_life" : end_of_life,
                "extended_support_end_date": extended_support_end_date
            }
            for server_environment, agent_id ,agent_name, ip_address, end_of_life, extended_support_end_date, server_owner, client_name, cs_owner, wazuh_status in rows
        ]

