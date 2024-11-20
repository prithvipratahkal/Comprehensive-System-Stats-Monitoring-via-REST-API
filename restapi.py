"""
This program runs on an Amazon Linux image and provides system stats.
"""
import json
import logging
from bottle import *
from system_stats import get_memory_usage, get_cpu_usage, get_all_stats
from system_stats import get_network_usage, get_disk_usage

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
    """
    Validates the API key provided in the request header.
     
    Raises:
        HTTPResponse: If the API key is missing or invalid, returns a 401 status
                      with an appropriate error message in JSON format.
    """
    api_key = request.get_header('x-api-key')

    if not api_key:
        logging.warning("No API key provided")
        response_data = {'status': 'error', 'message': 'Unauthorized: Missing API key'}
        raise HTTPResponse(
            status=401, body=json.dumps(response_data), content_type='application/json')

    if api_key != "my-secret-key":
        logging.warning("Invalid API key: %s ",api_key)
        response_data = {'status': 'error', 'message': 'Unauthorized: Invalid API key'}
        raise HTTPResponse(
            status=401, body=json.dumps(response_data), content_type='application/json')

@route('/system-stats')
def system_stats():
    """
    Fetches and returns system statistics based on query parameters.

    Query Parameters:
        include_cpu: If present, includes CPU usage in the response.
        include_memory: If present, includes memory usage in the response.
        include_disk: If present, includes disk usage in the response.
        include_network: If present, includes network stats in the response.

    Returns:
        str: JSON-formatted string containing the requested statistics
             or an error message in case of failure.
    """
    response.content_type = 'application/json'
    valid_params = {'include_cpu', 'include_memory', 'include_disk', 'include_network'}
    query_params = set(request.query.keys())

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
            return json.dumps(
                {'status': 'error', 'message': 'No stats collected, check your parameters'},
                indent=4)

    except Exception as e:
        logging.error("Error occurred %s",e)
        response.status = 500
        return json.dumps({'status': 'error', 'message': 'Internal error occurred'}, indent=4)

if __name__ == '__main__':
    run(host='0.0.0.0', port='9090')
