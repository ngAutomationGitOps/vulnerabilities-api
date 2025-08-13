from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.orm import joinedload
from sqlalchemy import func 
from app.models import SuriEvents



async def get_suri_events_count(session: AsyncSession, severity_label):
    if severity_label:
        return await SuriEvents.count(session , severity_label)
    else:
        return await SuriEvents.count(session, None)

async def get_so_events_map(session: AsyncSession):
    rows = await SuriEvents.so_events_map(session)
    return [
        { DestCountry : events_count }
        for DestCountry, events_count in rows
    ]

async def get_so_events_by_rule_tag(session: AsyncSession):
    rows , total = await SuriEvents.so_events_by_rule_tag(session)
    if total == 0:
        return {}
    return {
        rule_tag: round((count / total) * 100, 2)
        for rule_tag, count in rows
    }
    
async def get_so_events_by_severity_label(session: AsyncSession):
    rows , total = await SuriEvents.so_events_by_severity_label(session)
    if total == 0:
        return {}
    return {
        severity_label: round((count / total) * 100, 2)
        for severity_label, count in rows
    }
    
async def get_unique_ip(session: AsyncSession, ip_direction):
        return await SuriEvents.unique_ip(session , ip_direction)
    
async def get_alert_rules(session: AsyncSession):
    rows = await SuriEvents.alert_rules(session)
    return [
        {
            "Alert_rule_name" : alert_rule_name,
            "Rule_category" : rule_category,
            "Rule_confidence" : rule_confidence,
            "Reference" : reference,
            "Count" : count,
        }
        for alert_rule_name, rule_category, rule_confidence, reference, count in rows
    ]
    
async def get_ip_info(session: AsyncSession):
    rows = await SuriEvents.ip_info(session)
    return [
        {
            "Source_ip" : source_ip,
            "Source_port" : source_port,
            "Dest_Country" : dest_country,
            "Dest_ip" : dest_ip,
            "Dest_org" : dest_org,
            "Dest_port" : dest_port,
            "Count": count
        }
        for source_ip, source_port, dest_country, dest_ip, dest_org, dest_port, count in rows
    ]