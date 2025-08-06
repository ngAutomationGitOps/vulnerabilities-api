from app.models.vulnerabilities import Vulnerability
from app.models.detections import Detection
from app.models.combined import Combined

def get_severity_stats_by_os(filters: dict = {}):
    return Vulnerability.get_os_grouped_summary(filters)

def get_os_stats_by_severity():
    return Vulnerability.get_severity_grouped_summary()

def get_vuln_by_owner():
    return Combined.get_severity_summary_by_owner()