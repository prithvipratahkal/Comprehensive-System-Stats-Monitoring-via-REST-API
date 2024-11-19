import psutil
import time
import logging

logging.basicConfig(level=logging.INFO)

def get_all_stats():
    return [get_cpu_usage(),
        get_memory_usage(),
        get_disk_usage(),
        get_network_usage()]
        

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    logging.info(f"CPU usage is {cpu_usage}%")
    return {
        "cpu": cpu_usage
    }

def get_memory_usage():
    memory_info = psutil.virtual_memory()
    logging.info(f"Memory usage is {memory_info}")
    return {
        "memory": memory_info._asdict()
    }

def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    disk_used = disk_usage.used
    logging.info(f"Disk usage is {disk_used}")
    return { 
        "disk": disk_usage._asdict()
    }

def get_network_usage():
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
    logging.info(f"Network bandwidth is {mb_recv}")
    return {
        "network": mb_recv
    }

