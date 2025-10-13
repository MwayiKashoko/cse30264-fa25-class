#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import socket

def register_with_orchestrator(orch_ip, orch_port, worker_ip, worker_port, worker_id):
    msg = f"REGISTER {worker_ip} {worker_port} {worker_id}"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(msg.encode(), (orch_ip, orch_port))
            s.settimeout(2.0)
            data, _ = s.recvfrom(1024)
            print(f"[+] Registered {worker_id} -> {data.decode()}")
    except:
        print(f"[!] Failed to register {worker_id}")

if len(sys.argv) != 6:
    print(f"Usage: {sys.argv[0]} <orchestrator_ip> <orchestrator_port> <worker_ip> <starting_port> <num_workers>")
    sys.exit(1)

orch_ip = sys.argv[1]
orch_port = int(sys.argv[2])
worker_ip = sys.argv[3]
start_port = int(sys.argv[4])
num_workers = int(sys.argv[5])
num_workers = max(1, min(num_workers, 5))

os.makedirs("logs", exist_ok=True)

pids = []

for i in range(num_workers):
    worker_port = start_port + i
    worker_id = f"worker_{i+1}"
    log_dir = f"logs/{worker_id}"
    os.makedirs(log_dir, exist_ok=True)

    cmd = [
        "./server",
        str(worker_port),
        log_dir,
        worker_ip,
        orch_ip,
        str(orch_port),
        worker_id
    ]
    
    proc = subprocess.Popen(cmd)
    pids.append(proc.pid)
    time.sleep(0.3)

    register_with_orchestrator(orch_ip, orch_port, worker_ip, worker_port, worker_id)

print(f"{len(pids)} workers launched. PIDs: {pids}")
