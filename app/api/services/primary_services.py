from app.models.agents import Agent
from app.models.vulnerabilities import Vulnerability
from app.models.detections import Detection
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os

security = HTTPBasic()


def get_all_agents(query: dict = {}):
    return Agent.get_all(query)

def get_cve_count(query={}):
    return Vulnerability.count(query)

def get_vulnerability_count(query={}):
    return Detection.count(query)

def get_server_count(query={}):
    return Agent.count(query)

def get_status(query={}):
    status_counts = Detection.count_by_status(query)

    return {
        "open": status_counts.get("pending", 0),
        "closed": status_counts.get("resolved", 0)
    }


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    correct_username = secrets.compare_digest(credentials.username, os.getenv("SWAGGER_USER", "admin"))
    correct_password = secrets.compare_digest(credentials.password, os.getenv("SWAGGER_PASS", "secret"))

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def get_all_cve_summaries(query={}, skip=0, limit=100):
    return Vulnerability.get_all_summaries(query, skip, limit)


