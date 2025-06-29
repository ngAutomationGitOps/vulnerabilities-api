# app/api/routes.py
from app.api.handlers.stats_handler import get_os_grouped_summary , get_severity_grouped_summary


stats_routes = [
    {
        "method": "GET",
        "url": "/vuln-stats/severity-by-os",
        "handler": get_os_grouped_summary
    },
    {
        "method": "GET",
        "url": "/vuln-stats/os-by-severity",
        "handler": get_severity_grouped_summary
    }
]
