# app/api/routes.py
from app.api.handlers.primary_handler import server_check , get_agents , cve_count , vulnerability_count , server_count , get_status_vulnerabilities , get_docs, get_redoc , get_all_cves


primary_routes = [
     {
        "method": "GET",
        "url": "/docs",
        "handler": get_docs,
        "include_in_schema": False
    },
    {
        "method": "GET",
        "url": "/redoc",
        "handler": get_redoc,
        "include_in_schema": False
    },
    {
        "method": "GET",
        "url": "/",
        "handler": server_check
    },
    
    {
        "method" : "GET",
        "url": "/get-Agents",
        "handler": get_agents
    },
    
    {
    "method": "GET",
    "url": "/cve-count",
    "handler": cve_count
    },
    
    {
    "method": "GET",
    "url": "/vulnerability-count",
    "handler": vulnerability_count
    },
    
    {
    "method": "GET",
    "url": "/server-count",
    "handler": server_count
    },
    
    {
    "method": "GET",
    "url": "/status",
    "handler": get_status_vulnerabilities
    },
    
    {
    "method": "GET",
    "url": "/vuln-summary",
    "handler": get_all_cves
    }



]
