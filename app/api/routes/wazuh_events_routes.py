from app.api.handlers.wazuh_events_handlers import get_wazuh_events_count_handler , get_user_count_handler , get_events_by_user_handler,get_events_by_srcip_handler,get_events_by_status_handler, get_events_by_dept_handler,get_events_map_handler,get_impacted_servers_handler, get_recent_events_handler


wazuh_events_routes = [
    {
        "method" : "GET",
        "url": "/event-count",
        "handler": get_wazuh_events_count_handler
    },
    {
        "method" : "GET",
        "url": "/user-count",
        "handler": get_user_count_handler
    },
    {
        "method" : "GET",
        "url": "/events-by-user",
        "handler": get_events_by_user_handler
    },
    {
        "method" : "GET",
        "url": "/events-by-srcip",
        "handler": get_events_by_srcip_handler
    },
    {
        "method" : "GET",
        "url": "/events-by-status",
        "handler": get_events_by_status_handler
    },
    {
        "method" : "GET",
        "url": "/events-by-dept",
        "handler": get_events_by_dept_handler
    },
    {
        "method" : "GET",
        "url": "/events-map",
        "handler": get_events_map_handler
    },
    {
        "method" : "GET",
        "url": "/impacted-servers",
        "handler": get_impacted_servers_handler
    },
    {
        "method" : "GET",
        "url": "/recent-events",
        "handler": get_recent_events_handler
    }
    
]