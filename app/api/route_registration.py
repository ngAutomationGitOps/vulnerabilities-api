# app/api/route_registration.py
from fastapi import FastAPI
from app.api.routes.primary_routes import primary_routes
from app.api.routes.stat_routes import stats_routes
from app.api.routes.wazuh_events_routes import wazuh_events_routes
from app.api.routes.suri_events_routes import suri_events_routes
from app.api.routes.agents_routes import agents_routes
from fastapi import HTTPException

def register_routes(app: FastAPI):
    all_routes = primary_routes + stats_routes +wazuh_events_routes + suri_events_routes + agents_routes
    for route in all_routes:
        if route["method"] == "GET":
            app.add_api_route(route["url"], route["handler"], methods=["GET"])
        else:
            raise HTTPException(status_code=405, detail="Method not allowed")
