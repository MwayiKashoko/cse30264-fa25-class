#!/usr/bin/env python3
import socket
import argparse
import datetime
import threading

# Argument parsing
parser = argparse.ArgumentParser(description="Orchestrator for worker pool")
parser.add_argument('--port', type=int, required=True, help='Port to listen on')
args = parser.parse_args()

orch_ip = "0.0.0.0"
orch_port = args.port

worker_pool = {}  # worker_id -> { address: (ip, port), last_sent, last_received }
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((orch_ip, orch_port))
sock.settimeout(1.0)  # so we can break cleanly if needed

print(f"[+] Orchestrator listening on {orch_ip}:{orch_port}")

# Helper functions
def now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def register_worker(ip, port, worker_id):
    #Register a worker in the pool.
    worker_pool[worker_id] = {
        'address': (ip, port),
        'last_sent': 'N/A',
        'last_received': now_str()
    }
    print(f"[REGISTER] Worker {worker_id} at {ip}:{port}")

def forward_to_worker(worker_id, message, client_addr):
    """Forward message to worker and relay response back to client."""
    worker_info = worker_pool.get(worker_id)
    if not worker_info:
        sock.sendto(b"400 ERROR Worker not found", client_addr)
        return

    worker_addr = worker_info['address']
    sock.sendto(message.encode(), worker_addr)
    worker_info['last_sent'] = now_str()

    try:
        data, _ = sock.recvfrom(4096)
        response = data.decode()
        worker_info['last_received'] = now_str()
        sock.sendto(response.encode(), client_addr)
    except socket.timeout:
        sock.sendto(b"400 ERROR Worker timeout", client_addr)

def pool_status():
    #Build a status string of the worker pool.
    if not worker_pool:
        return "400 ERROR No workers registered"
    lines = []
    for wid, info in worker_pool.items():
        ip, port = info['address']
        lines.append(
            f"{wid} {ip}:{port} last_sent={info['last_sent']} last_received={info['last_received']}"
        )
    return "\n".join(lines)

# Main loop
while True:
    try:
        data, addr = sock.recvfrom(4096)
    except socket.timeout:
        continue

    msg = data.decode().strip()
    print(f"[CLIENT {addr}] -> {msg}")

    # Worker registration: "REGISTER <ip> <port> <worker_id>"
    if msg.startswith("REGISTER"):
        try:
            _, w_ip, w_port, w_id = msg.split()
            register_worker(w_ip, int(w_port), w_id)
            sock.sendto(b"200 OK", addr)
        except Exception as e:
            sock.sendto(f"400 ERROR REGISTER {e}".encode(), addr)

    # Pool status request
    elif msg == "POOL_STATUS":
        response = pool_status()
        sock.sendto(response.encode(), addr)

    # Forward client commands to workers
    elif msg.startswith("CHECK") or msg.startswith("LAST_HITS"):
        if not worker_pool:
            sock.sendto(b"400 ERROR No workers available", addr)
        else:
            first_worker = next(iter(worker_pool.keys()))
            forward_to_worker(first_worker, msg, addr)

    else:
        sock.sendto(b"400 ERROR Unknown command", addr)
