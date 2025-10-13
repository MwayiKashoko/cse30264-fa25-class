#!/usr/bin/env python3
import sys
import socket

if len(sys.argv) != 3:
    print("Usage: python3 pool-status.py <orchestrator_host> <orchestrator_port>")
    sys.exit(1)

orch_host = sys.argv[1]
orch_port = int(sys.argv[2])

try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5.0)
        # Send a special command to orchestrator
        sock.sendto(b"POOL_STATUS", (orch_host, orch_port))

        data, _ = sock.recvfrom(4096)
        response = data.decode()
        print("Worker Pool Status:\n")
        for line in response.strip().split("\n"):
            print(line)
except socket.timeout:
    print("No response from orchestrator (timeout)")
except Exception as e:
    print(f"Error: {e}")