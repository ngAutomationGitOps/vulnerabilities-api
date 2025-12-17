from app.api.handlers.asm_handler import get_domains_count_handler , get_ssl_issues_count_handler , get_critical_severities_count_handler, get_open_ports_count_handler , get_outdated_tech_count_handler, get_categorized_ports_handler, get_vulnerabilities_by_severity_handler,get_ports_by_domain_handler , get_top_vulnerabilities_handler


asm_routes = [
    {
        "method" : "GET",
        "url": "/asm-domains-count",
        "handler":get_domains_count_handler
    },
    {
        "method" : "GET",
        "url": "/asm-ssl-issues-count",
        "handler":get_ssl_issues_count_handler
    },
    {
        "method" : "GET",
        "url": "/asm-critical-count",
        "handler":get_critical_severities_count_handler
    },
    {
        "method" : "GET",
        "url": "/asm-open-ports",
        "handler":get_open_ports_count_handler
    },
    {
        "method" : "GET",
        "url": "/asm-outdated_tech",
        "handler":get_outdated_tech_count_handler
    },
    {
        "method" : "GET",
        "url": "/asm-categorized_ports",
        "handler":get_categorized_ports_handler
    },
    {
        "method" : "GET",
        "url": "/asm-vuln_by_severity",
        "handler": get_vulnerabilities_by_severity_handler
    },
    {
        "method" : "GET",
        "url": "/asm-ports_by_domain",
        "handler": get_ports_by_domain_handler
    },
    {
        "method" : "GET",
        "url": "/asm-top_vuln",
        "handler": get_top_vulnerabilities_handler
    }
    
]