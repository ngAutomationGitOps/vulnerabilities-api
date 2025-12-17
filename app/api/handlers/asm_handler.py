from app.utilities.postgresql import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends
from app.api.services.asm_services import get_domains_count , get_ssl_issues_count , get_critical_severities_count, get_open_ports_count , get_outdated_tech_count, get_categorized_ports, get_vulnerabilities_by_severity, get_ports_by_domain , get_top_vulnerabilities

async def get_domains_count_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    domains = await get_domains_count(db)
    return {"domains_count": domains}

async def get_ssl_issues_count_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    ssl_issues = await get_ssl_issues_count(db)
    return {"ssl_issues_count": ssl_issues}

async def get_critical_severities_count_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    critical_severities = await get_critical_severities_count(db)
    return {"critical_count": critical_severities}

async def get_open_ports_count_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    open_ports = await get_open_ports_count(db)
    return {"open_ports": open_ports}

async def get_outdated_tech_count_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    outdated_tech = await get_outdated_tech_count(db)
    return {"open_ports": outdated_tech}

async def get_categorized_ports_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    categorized_ports = await get_categorized_ports(db)
    return {"categorized_ports": categorized_ports}

async def get_vulnerabilities_by_severity_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    vuln_by_severities = await get_vulnerabilities_by_severity(db)
    return {"vuln_by_severities": vuln_by_severities}

async def get_ports_by_domain_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    ports_by_domain = await get_ports_by_domain(db)
    return {"ports_by_domain": ports_by_domain}
    
async def get_top_vulnerabilities_handler(req: Request, db: AsyncSession = Depends(get_db)):
    query_params = dict(req.query_params)
    top_vulns = await get_top_vulnerabilities(db)
    return {"top_vulns": top_vulns}