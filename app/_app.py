'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from app.utilities.jwt_secret_generator import generate_jwt_secret
#from app.configurations.rabbitmq_gateway import connect_rabbitmq
#from app.configurations.socketio import socketio_connection
#from app.utilities.sync_models import sync_models
import os
from dotenv import load_dotenv
from app.api.route_registration import register_routes

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[os.getenv("ALLOWED_CLIENT")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register Routes
    register_routes(app)

    # Application startup events
    @app.on_event("startup")
    async def on_startup():
        print("Generated JWT secret:")

    return app
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from app.api.route_registration import register_routes

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🟢 Startup logic
    print("Generated JWT secret:")
    yield
    # 🔴 Shutdown logic (optional)
    print("Shutting down app")

def create_app(
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json"
) -> FastAPI:
    app = FastAPI(
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
        lifespan=lifespan  
    )

    app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_CLIENT", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


    # Register Routes
    register_routes(app)
    return app
