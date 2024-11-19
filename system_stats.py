"""
Module to fetch system statistics such as CPU, memory, disk, and network usage.
"""

import time
import logging
import psutil

logging.basicConfig(level=logging.INFO)

def get_all_stats():
    """
    Fetches all system statistics, including CPU, memory, disk, and network usage.

    Returns:
        list: A list of dictionaries containing all system stats.
    """
    return [get_cpu_usage(),
        get_memory_usage(),
        get_disk_usage(),
        get_network_usage()]

def get_cpu_usage():
    """
    Fetches the CPU usage percentage.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    logging.info("CPU usage is %s%%", cpu_usage)
    return {
        "cpu": cpu_usage
    }

def get_memory_usage():
    """
    Fetches memory usage statistics.
    """
    memory_info = psutil.virtual_memory()
    logging.info("Memory usage is %s",memory_info)
    return {
        "memory": memory_info._asdict()
    }

def get_disk_usage():
    """
    Fetches disk usage statistics for the root directory.
    """
    disk_usage = psutil.disk_usage('/')
    disk_used = disk_usage.used
    logging.info("Disk usage is %s", disk_used)
    return {
        "disk": disk_usage._asdict()
    }

def get_network_usage():
    """
    Calculates the amount of network data received in the past second.
    """
    # Get initial network stats
    start = psutil.net_io_counters()

    # Wait for 1s
    time.sleep(1)

    # Get network stats again
    end = psutil.net_io_counters()

    # Calculate the amount of data sent and received
    bytes_received = end.bytes_recv - start.bytes_recv

    # Convert bytes to megabytes for easier readability
    mb_recv = bytes_received / (1024 ** 2)
    logging.info("Network bandwidth is %s", mb_recv)
    return {
        "network": mb_recv
    }
