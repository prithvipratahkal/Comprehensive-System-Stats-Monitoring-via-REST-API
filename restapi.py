# This program is written for Amazon Linux image

from bottle import * 
from system_stats import *
import logging
import json
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

logging.basicConfig(
    filename=f'restapi_{timestamp}.log',
    level=logging.INFO,        
    format='%(asctime)s - %(levelname)s - %(message)s'
)

from bottle import HTTPResponse

@hook('before_request')
def validate_api_key():
    api_key = request.get_header('x-api-key')
    logging.info(f'api key is {api_key}')
    
    if not api_key:
        logging.warning("No API key provided")
        response_data = {'status': 'error', 'message': 'Unauthorized: Missing API key'}
        raise HTTPResponse(status=401, body=json.dumps(response_data), content_type='application/json')
    
    if api_key != "my-secret-key":
        logging.warning(f"Invalid API key: {api_key}")
        response_data = {'status': 'error', 'message': 'Unauthorized: Invalid API key'}
        raise HTTPResponse(status=401, body=json.dumps(response_data), content_type='application/json')
    

@route('/system-stats')
def system_stats():
    response.content_type = 'application/json'
    valid_params = {'include_cpu', 'include_memory', 'include_disk', 'include_network'}
    query_params = set(request.query.keys())
    logging.info(f"valid params {query_params}")

    # Check for invalid parameters
    if not query_params.issubset(valid_params) and query_params:
        response.status = 400
        return json.dumps({'status': 'error', 'message': 'Invalid parameters provided'}, indent=4)

    include_cpu = request.query.get('include_cpu')
    include_memory = request.query.get('include_memory')
    include_disk = request.query.get('include_disk')
    include_network = request.query.get('include_network')

    stats = []
    try:
        if include_cpu:
            logging.info("Checking CPU usage")
            cpu = get_cpu_usage()
            stats.append(cpu)

        if include_memory:
            logging.info("Checking memory usage")
            stats.append(get_memory_usage())

        if include_disk:
            logging.info("Checking disk usage")
            stats.append(get_disk_usage())

        if include_network:
            logging.info("Checking bandwidth usage")
            stats.append(get_network_usage())

        if len(stats) == 0:
            logging.info("Sending all stats")
            all_stats = get_all_stats()
            if all_stats is not None:
                stats.append(all_stats)

        if stats and any(stat is not None for stat in stats):
            system_stats = {
                "stats": stats
            }
            response.status = 200
            return json.dumps(system_stats, indent=4)
        else:
            logging.warning("No stats collected")
            response.status = 500
            return json.dumps({'status': 'error', 'message': 'No stats collected, check your parameters'}, indent=4)

    except Exception as e:
        logging.error(f"Error occurred {e}")
        response.status = 500
        return json.dumps({'status': 'error', 'message': 'Internal error occurred'}, indent=4)

if __name__ == '__main__': 
    run(host='0.0.0.0', port='9090')
