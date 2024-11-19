URL: /system-stats

Method: GET

Query Parameters:

include_cpu (optional): Include CPU usage stats (e.g., include_cpu=true)
include_memory (optional): Include memory usage stats (e.g., include_memory=true)
include_disk (optional): Include disk usage stats (e.g., include_disk=true)
include_network (optional): Include network usage stats (e.g., include_network=true)

If no query parameters are provided, the API will return all available system stats. 

Ex: 
curl "http://localhost:9090/system-stats?include_cpu=true&include_memory=true"

output:
{
    "stats": [
        {
            "cpu": 0.0
        },
        {
            "memory": {
                "total": 995610624,
                "available": 700964864,
                "percent": 29.6,
                "used": 148299776,
                "free": 551575552,
                "active": 169230336,
                "inactive": 158130176,
                "buffers": 2220032,
                "cached": 293515264,
                "shared": 458752,
                "slab": 66404352
            }
        }
    ]
}

