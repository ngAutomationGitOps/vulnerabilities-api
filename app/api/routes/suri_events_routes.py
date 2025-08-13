from app.api.handlers.suri_events_handlers import get_suri_events_count_handler,get_so_events_map_handler ,get_so_events_by_rule_tag_handler, get_so_events_by_severity_label_handler, get_unique_ip_handler

suri_events_routes = [
    {
        "method" : "GET",
        "url": "/so-event-count",
        "handler": get_suri_events_count_handler
    },
    {
        "method" : "GET",
        "url": "/so-events-map",
        "handler": get_so_events_map_handler
    },
    {
        "method" : "GET",
        "url": "/so-events-by-rule",
        "handler": get_so_events_by_rule_tag_handler
    },
    {
        "method" : "GET",
        "url": "/so-events-by-label",
        "handler": get_so_events_by_severity_label_handler
    },
    {
        "method" : "GET",
        "url": "/unique-ip",
        "handler": get_unique_ip_handler
    }
]
