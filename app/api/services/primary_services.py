from sqlalchemy.future import select
from app.models.agents import Agent as AgentModel
from sqlalchemy.ext.asyncio import AsyncSession 
from app.models.fim import Fim
from sqlalchemy.orm import joinedload
from sqlalchemy import func 
from app.models.fim import Fim
from app.models.agents import Agent
from app.models.department import Department
from app.models import Vulnerability
from app.models import Detection

SEVERITY_MAP = {
    1: "Critical",
    2: "High",
    3: "Medium",
    4: "Low"
}

async def get_all_agents_postgres(session: AsyncSession, query: dict = {}):
    result = await session.execute(select(AgentModel))
    agents = result.scalars().all()
    return agents


async def get_fim_count(session: AsyncSession):
    return await Fim.count(session)

async def get_fim_event_counts(cls, session: AsyncSession):
        stmt = select(cls.event, func.count()).group_by(cls.event)
        result = await session.execute(stmt)
        rows = result.all()
        return {event: count for event, count in rows}
    
async def get_fim_event_counts_service(db):
    result = await Fim.get_grouped_event_counts(db)
    rows = result.all()
    return {event: count for event, count in rows}

async def get_fim_events(session: AsyncSession, query: dict = {}):
    rows = await Fim.get_fim_events(session)
    return [
            {
                "agent_name": r.agent_name,
                "department": r.department,
                "server_owner": r.name,
                "description": r.description,
                "path": r.path,
                "detected_at": r.detected_at
            }
            for r in rows
        ]
    


async def get_fim_event_percentages_by_department(session: AsyncSession):
    rows , total = await Fim.get_fim_event_percentages(session)

    if total == 0:
        return {}

    return {
        department_name: round((count / total) * 100, 2)
        for department_name, count in rows
    }
    
    
async def get_vulnerability_count_by_severity(session, severity_id: int):
    severity_status = SEVERITY_MAP.get(severity_id)
    if not severity_status:
        raise ValueError(f"Invalid severity ID: {severity_id}")
    return await Vulnerability.count_vulnerabilities_by_severity(session, severity_status)
    
async def get_vuln_count(session: AsyncSession):
    return await Vulnerability.count(session)

async def get_vuln_percentages_by_department(session: AsyncSession):
    rows , total = await Detection.get_vuln_percentages(session)
    if total == 0:
        return {}
    return {
        department_name: round((count / total) * 100, 2)
        for department_name, count in rows
    }
    
    
async def get_vuln_by_os(session: AsyncSession):
    rows = await Detection.get_vuln_by_os(session)
    totals = {}
    for severity, os_name, count in rows:
        totals[severity] = totals.get(severity, 0) + count
    data = {}
    for severity, os_name, count in rows:
        percent = (count / totals[severity] * 100) if totals[severity] > 0 else 0
        data.setdefault(severity, {})[os_name] = percent

    return data
    