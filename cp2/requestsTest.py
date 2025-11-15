import requests
import time
import statistics

url = "http://127.0.0.1:5000"

urls = {
    "data": "/data",
    "mean": "/dl/stat/mean?month=5&year=2024&iface=wlan0",
    "peak": "/dl/stat/peak?month=5&year=2024&iface=wlan0"
}

trials = 15
trialResults = {}

for name, endpoint in urls.items():
    times = []
    print(f"Testing endpoint '{name}' {trials} times...")
    for i in range(trials):
        start = time.time()
        try:
            r = requests.get(url + endpoint)
            r.raise_for_status()
        except Exception as e:
            print(f"Request failed: {e}")
            continue
        end = time.time()
        times.append(end - start)
    if times:
        trialResults[name] = times

# Print statistics
for name, times in trialResults.items():
    print(f"\nEndpoint: {name}")
    print(f"Min:    {min(times):.4f} s")
    print(f"Max:    {max(times):.4f} s")
    print(f"Mean:   {statistics.mean(times):.4f} s")
    print(f"Median: {statistics.median(times):.4f} s")
    if len(times) > 1:
        print(f"Stddev: {statistics.stdev(times):.4f} s")
    else:
        print("Stddev: N/A")
