from app.api.handlers.agents_handler import get_agents_count_handler , get_all_agents_count_handler,get_agent_status_by_dept_handler,get_agent_by_env_handler, get_agent_by_dept_handler, get_agent_info_handler


agents_routes = [
    {
        "method" : "GET",
        "url": "/agents-count",
        "handler": get_all_agents_count_handler
    },
    {
        "method" : "GET",
        "url": "/agents-count/{origin}",
        "handler": get_agents_count_handler
    },
    {
        "method" : "GET",
        "url": "/agents-status-by-dept",
        "handler": get_agent_status_by_dept_handler
    },
    {
        "method" : "GET",
        "url": "/agents-by-env",
        "handler": get_agent_by_env_handler
    },
    {
        "method" : "GET",
        "url": "/agents-by-dept",
        "handler": get_agent_by_dept_handler
    },
    {
        "method" : "GET",
        "url": "/agents-info",
        "handler": get_agent_info_handler
    }
]
