# app/api/routes.py
from app.api.handlers.primary_handler import get_agents


primary_routes = [
    {
        "method" : "GET",
        "url": "/get-Agents",
        "handler": get_agents
    },
]
