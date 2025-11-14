from flask import Flask, request, jsonify
import json
from datetime import datetime

portNumber = 5000
files = ["data/set1/data-10.json"]

app = Flask(__name__)

#get all JSON files

records = []
for f in files:
    with open(f, "r") as fp:
        records.extend(json.load(fp))

print(records)

@app.route("/")
def getData():
    pass