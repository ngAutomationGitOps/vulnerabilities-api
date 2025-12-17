# app/api/routes.py
from app.api.handlers.primary_handler import get_agents , get_fim_count_handler , get_fim_eventsCount_handler, get_fim_events_handler , get_fim_event_percent_by_department_handler, get_vulnerability_count_handler , get_vuln_count_handler, get_vuln_percent_by_department_handler,get_vuln_by_os_handler, get_vuln_by_dept_handler , get_cve_ids_handler, get_vuln_desc_handler


primary_routes = [
    {
        "method" : "GET",
        "url": "/get-Agents",
        "handler": get_agents
    },
    {
       "method" : "GET",
        "url": "/fim-count",
        "handler": get_fim_count_handler 
    },
    {
       "method" : "GET",
        "url": "/fim-eventCount",
        "handler": get_fim_eventsCount_handler
    },
    {
        "method" : "GET",
        "url": "/fim-events",
        "handler": get_fim_events_handler
    },
    {
        "method": "GET",
        "url": "/fim-by-department",
        "handler": get_fim_event_percent_by_department_handler
    },
    {
        "method": "GET",
        "url": "/vuln-count/{severity_id}",
        "handler": get_vulnerability_count_handler
    },
    {
       "method": "GET",
        "url": "/vuln-count",
        "handler": get_vuln_count_handler
    },
    {
        "method": "GET",
        "url": "/vuln-by-department",
        "handler": get_vuln_percent_by_department_handler
    },
    {
        "method": "GET",
        "url": "/vuln-by-os",
        "handler": get_vuln_by_os_handler
    },
    
    {
        "method": "GET",
        "url": "/vuln-by-dept",
        "handler": get_vuln_by_dept_handler
    },
    {
        "method": "GET",
        "url": "/cve-ids",
        "handler": get_cve_ids_handler
    },
    {
        "method": "GET",
        "url": "/vuln_desc",
        "handler": get_vuln_desc_handler
    }
]
