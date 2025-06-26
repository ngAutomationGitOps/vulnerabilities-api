# app/api/routes.py
from app.api.handlers.primary_handler import server_check , get_agents


routes = [
    {
        "method": "GET",
        "url": "/",
        "handler": server_check
    },
    
    {
        "method" : "GET",
        "url": "/get-Agents",
        "handler": get_agents
    }
]
