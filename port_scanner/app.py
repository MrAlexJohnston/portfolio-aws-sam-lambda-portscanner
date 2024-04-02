import os
import json
import socket
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger()
logger.setLevel(logging.INFO)

max_workers = int(os.environ.get('MAX_WORKERS', '100'))

def scan_port(target, port, open_ports):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Adjust timeout as needed
            result = s.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
                logger.info(f"Found port {port}")
    except Exception as e:
        logger.error(f"Error scanning port {port}: {e}")

def lambda_handler(event, context):
    # Extract target from event
    target = event.get("target", "")
    if not target:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "No target specified."})
        }

    try:
        resolved_target = socket.gethostbyname(target)
        logger.info(f"Scanning target: {target} -> {resolved_target}")
    except socket.gaierror:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Target host could not be resolved."})
        }

    open_ports = []

    # Scan ports
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for port in range(0, 65535):
            executor.submit(scan_port, resolved_target, port, open_ports)
    
    logger.info(f"List of open ports: {open_ports}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Scan complete for target: {resolved_target}",
            "open_ports": open_ports
        }),
    }