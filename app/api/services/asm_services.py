from app.models.asm_domain import ASMDomains
from app.models.asm_ssl_info import ASMSslInfo
from app.models.asm_vulnerabilities import ASMVulnerabilities
from app.models.asm_open_ports import ASMOpenPorts
from app.models.asm_technologies import ASMTechnologies
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.orm import joinedload
from sqlalchemy import func 

PORT_CATEGORIES = {
    21:  "FTP",
    25:  "SMTP",
    53:  "DNS",
    80:  "HTTP",
    110: "POP3",
    115: "SFTP",
    143: "IMAP",
    443: "HTTPS",
    465: "SMTPS",
    993: "IMAPS",
    995: "POP3S"
}

async def get_domains_count(session: AsyncSession):
    return await ASMDomains.count(session)

async def get_ssl_issues_count(session: AsyncSession):
    return await ASMSslInfo.issues_count(session)

async def get_critical_severities_count(session: AsyncSession):
    return await ASMVulnerabilities.critical_severities_count(session)

async def get_open_ports_count(session: AsyncSession):
    return await ASMOpenPorts.count(session)

async def get_outdated_tech_count(session: AsyncSession):
    return await ASMTechnologies.outdated_tech(session)

async def get_categorized_ports(session: AsyncSession):
    rows = await ASMOpenPorts.port_category_counts(session)
    output = {}
    for port, count in rows:
        if port in PORT_CATEGORIES:
            key = f"{PORT_CATEGORIES[port]} - {port}"
        else:
            key = f"Custom - {port}"
        output[key] = count
    return output


async def get_vulnerabilities_by_severity(session: AsyncSession):
    rows = await ASMVulnerabilities.vulnerabilities_by_severity(session)
    return {
        severity_label: count
        for severity_label, count in rows
    }
    
async def get_ports_by_domain(session: AsyncSession):
    rows = await ASMOpenPorts.ports_by_domain(session)

    output = {}
    for domain_id, domain_name, port, count in rows:

        if domain_name not in output:
            output[domain_name] = {
                "default_ports": [],
                "custom_ports": [],
                "total": 0
            }

        if port in PORT_CATEGORIES:
            output[domain_name]["default_ports"].append(port)
        else:
            output[domain_name]["custom_ports"].append(port)
            
        output[domain_name]["total"] += count

    return output

async def get_top_vulnerabilities(session: AsyncSession):
    rows = await ASMVulnerabilities.top_vulnerabilities(session)
    return [
        {
            "Domain Name" : domain_name,
            "IP" : ip_address,
            "Issue" : issue,
            "Severity" : severity
        }
        for asm_id , domain_name ,  ip_address, severity , issue in rows
    ]
    

