#!/usr/bin/env python3
import sys
import socket

if len(sys.argv) != 4:
    print("Usage: python3 check-hits.py <orchestrator_host> <orchestrator_port> <N>")
    sys.exit(1)

orch_host = sys.argv[1]
orch_port = int(sys.argv[2])
N = max(1, min(int(sys.argv[3]), 5))

try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5.0)
        # Send request
        message = f"LAST_HITS {N}".encode()
        sock.sendto(message, (orch_host, orch_port))

        data, _ = sock.recvfrom(4096)
        response = data.decode().strip()

        print(f"Last {N} {'hits' if N > 1 else 'hit'} triggering image fetch:\n")
        if response.startswith("400"):
            print("400 ERROR — orchestrator has no hits recorded.")
        else:
            for line in response.split("\n"):
                print(line)

except socket.timeout:
    print("No response from orchestrator (timeout)")
except Exception as e:
    print(f"Error: {e}")