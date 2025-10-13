Coding Project 1 - Part 2

Name: Mwayi Kashoko (Worked alone)

## Description
This project implements a distributed ad-checking system:
- **C Worker Server (`server`)**: Fetches HTML pages and checks for the presence of a specified AdID.
- **Python Orchestrator (`orchestrator.py`)**: Maintains a pool of workers and forwards client requests.
- **Python Client (`client-v2.py`)**: Sends requests to the orchestrator and saves detected ad images.
- **Helper scripts**:
  - `launch-workers.py` → Launches 1–5 workers and registers them with the orchestrator.
  - `pool-status.py` → Displays current worker pool state.
  - `check-hits.py` → Displays last N hits.

---

lsof -i UDP:54106

## Compilation

use makefile to run

# Launch server
./server 54107 logs 127.0.0.1 127.0.0.1 54106 worker_1 &

# Start Orchestrator
python3 orchestrator.py --port <ORCH_PORT>
python3 orchestrator.py --port 54106 &

# Launch Workers
python3 launch-workers.py <ORCH_IP> <ORCH_PORT> <WORKER_IP> <START_PORT> <NUM_WORKERS>
### Example: launch 2 workers
python3 launch-workers.py 127.0.0.1 54106 127.0.0.1 54107 2

# Run Client
python3 client-v2.py <URL> <AdID> <SiteID> [--port PORT] [--server IP] [--tries N] [--gap SECONDS] [--verbose] [--showTime]
### Example:
python3 client-v2.py http://ns-mn1.cse.nd.edu/cse30264/ads/file1.html IRISH_CSE S1 --port 54106 --server 127.0.0.1 --tries 1 --gap 1 --verbose

# Check Worker Pool
python3 pool-status.py <ORCH_IP> <ORCH_PORT>
python3 pool-status.py 127.0.0.1 54106

# Check Last Hits
python3 check-hits.py <ORCH_IP> <ORCH_PORT> <N>
python3 check-hits.py 127.0.0.1 54106 5