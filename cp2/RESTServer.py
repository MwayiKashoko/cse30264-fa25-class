from flask import Flask, request, jsonify
import json
from datetime import datetime
from collections import defaultdict

portNumber = 5000
files = ["data/set1/data-10.json"]

app = Flask(__name__)

#get all JSON files

records = []
for f in files:
    with open(f, "r") as fp:
        records.extend(json.load(fp))

@app.route("/data")
def getData():
    month = request.args.get("m", type=int)
    day = request.args.get("d", type=int)
    year = request.args.get("y", type=int)
    dr = request.args.get("dir")
    iface = request.args.get("if")

    output = []

    for r in records:
        if r.get("type") != "iperf":
            continue

        timestamp = r.get("timestamp")

        try:
            time = datetime.fromisoformat(timestamp)
        except:
            continue

        if month and time.month != month:
            continue
        if day and time.day != day:
            continue
        if year and time.year != year:
            continue
        if dr and r.get("direction") != dr:
            continue
        if iface and r.get("interface") != iface:
            continue

        output.append(r)

    return jsonify(output)

@app.route("/dl/stat/mean")
def mean():
    month = request.args.get("month", type=int)
    day   = request.args.get("day", type=int)
    year  = request.args.get("year", type=int)
    iface = request.args.get("if")

    dailyValues = defaultdict(list)

    for r in records:
        if r.get("type") != "iperf":
            continue
        if r.get("direction") != "downlink":
            continue
        if iface and r.get("interface") != iface:
            continue

        ts = r.get("timestamp")
        try:
            t = datetime.fromisoformat(ts)
        except:
            continue

        if month and t.month != month:
            continue
        if day and t.day != day:
            continue
        if year and t.year != year:
            continue

        key = t.date()
        dailyValues[key].append(r.get("tput_mbps", 0))


    result = {str(day): sum(vals)/len(vals) for day, vals in dailyValues.items() if vals}

    return jsonify(result)

@app.route("/dl/stat/peak")
def peak():
    month = request.args.get("month", type=int)
    day   = request.args.get("day", type=int)
    year  = request.args.get("year", type=int)
    iface = request.args.get("if")

    dailyValues = defaultdict(list)

    for r in records:
        if r.get("type") != "iperf":
            continue
        if r.get("direction") != "downlink":
            continue
        if iface and r.get("interface") != iface:
            continue

        ts = r.get("timestamp")
        try:
            t = datetime.fromisoformat(ts)
        except:
            continue

        if month and t.month != month:
            continue
        if day and t.day != day:
            continue
        if year and t.year != year:
            continue

        key = t.date()
        dailyValues[key].append(r.get("tput_mbps", 0))

    result = {str(day): max(vals) for day, vals in dailyValues.items() if vals}

    return jsonify(result)