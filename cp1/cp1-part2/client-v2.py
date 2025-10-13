# client.py : Have the a worker server fetch the content and check to see if has our
# advertising ID
#
# Syntax:
#  python3 client.py URL AdID SiteID -port 41000 -server 127.0.0.1 -tries 5 -gap 1
#  python3 client.py http://ns-mn1.cse.nd.edu/cse30264/ads/file1.html IRISH_CSE S1 --port 54150 --server 127.0.0.1 --tries 1 --gap 1
#
# URL is required and is the URL to check
# AdID is the string to look for (must be contiguous)
# SiteID is a string (must be contiguous)
#
# --port   Optionally changes the port from 54000 to a specific value
# --server The IP or hostname of the server, default is localhost
# --tries  The number of times to fetch this site from the server (default is one)
# --gap    The gap between tries (default is 1 second)
#

import argparse
import os
import time
import socket
import re
import requests
import datetime
import urllib.parse

# -------------------------
# Argument parsing
# -------------------------
parser = argparse.ArgumentParser(description='Python client for confirming ad states')
parser.add_argument('URL', type=str, help='The URL to access')
parser.add_argument('AdID', type=str, help='The search string for our ads')
parser.add_argument('SiteID', type=str, help='The site ID to use for logging')
parser.add_argument('--port', type=int, default=54000, help='Port for the server')
parser.add_argument('--server', type=str, default='127.0.0.1', help='Hostname or IP address of server')
parser.add_argument('--tries', type=int, default=1, help='Number of times to check the site')
parser.add_argument('--gap', type=float, default=1.0, help='Gap between queries (in seconds)')
parser.add_argument('--showTime', action="store_true", help='Show elapsed time for each run')
parser.add_argument('--verbose', action="store_true", help='Enable verbose output')
args = parser.parse_args()

logsDir = "NOTSET"

if args.verbose:
    print(f'Running {args.tries} request(s) to {args.server}:{args.port}')

for theTry in range(args.tries):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect((args.server, args.port))

            theRequest = f"CHECK {args.URL} {args.AdID} {args.SiteID}"
            if args.verbose:
                print(f'[TRY {theTry+1}] Sending: {theRequest}')

            s.send(theRequest.encode('utf-8'))
            data, _ = s.recvfrom(4096)
            response = data.decode().strip()

            if response.startswith("LOGDIR123123321321"):
                logsDir = response.split(' ', 1)[1].split('\n')[0].strip()

            status = response.split("\n")[-1] if response else "400 ERROR No response"

            if "YES" in status and logsDir != "NOTSET":
                # fetch the HTML directly from the URL
                html = requests.get(args.URL, timeout=5).text

                # extract image src attributes
                images = []
                for tag in re.findall(r'<img[^>]+>', html, flags=re.IGNORECASE):
                    m = re.search(r'src=[\"\']?([^\"\'>]+)', tag, flags=re.IGNORECASE)
                    if m:
                        src = urllib.parse.urljoin(args.URL, m.group(1))
                        images.append(src)

                d = datetime.datetime.now()
                currDate = f"{d:%Y-%m-%d-%H-%M-%S}"
                currDir = f"{logsDir}/{args.SiteID}/{currDate}"
                os.makedirs(currDir, exist_ok=True)

                for imgURL in images:
                    try:
                        img_data = requests.get(imgURL, timeout=5).content
                        imgName = os.path.basename(urllib.parse.urlparse(imgURL).path)
                        filename = f"{currDir}/{imgName}"
                        with open(filename, "wb") as handler:
                            handler.write(img_data)
                        if args.verbose:
                            print(f'[IMG] Saved {filename}')
                    except Exception as e:
                        print(f'[!] Failed to download image {imgURL}: {e}')

                print(status, args.SiteID, currDate)
            else:
                print(status)

            if theTry + 1 < args.tries:
                time.sleep(args.gap)

    except socket.error as e:
        print(f"Socket error: {e}")
        print(f"Requested Host: {args.server}")
        print(f"Requested Port: {args.port}")