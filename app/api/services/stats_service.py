from app.models.vulnerabilities import Vulnerability

def get_severity_stats_by_os(filters: dict = {}):
    return Vulnerability.get_os_grouped_summary(filters)

def get_os_stats_by_severity():
    return Vulnerability.get_severity_grouped_summary()