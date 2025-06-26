# app/api/route_registration.py
from fastapi import FastAPI
from app.api.routes.primary_routes import routes
from fastapi import HTTPException

def register_routes(app: FastAPI):
    for route in routes:
        if route["method"] == "GET":
            app.add_api_route(route["url"], route["handler"], methods=["GET"])
        else:
            raise HTTPException(status_code=405, detail="Method not allowed")
