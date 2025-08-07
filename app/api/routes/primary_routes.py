# app/api/routes.py
from app.api.handlers.primary_handler import get_agents , get_fim_count_handler , get_fim_eventsCount_handler, get_fim_events_handler , get_fim_event_percent_by_department_handler


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
    }
]
