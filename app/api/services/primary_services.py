from app.models.agents import Agent
from app.models.vulnerabilities import Vulnerability
from app.models.detections import Detection

def get_all_agents(query: dict = {}):
    return Agent.get_all(query)

def get_cve_count(query={}):
    return Vulnerability.count(query)

def get_vulnerability_count(query={}):
    return Detection.count(query)

def get_vulnerability_count(query={}):
    return Vulnerability.count(query)
