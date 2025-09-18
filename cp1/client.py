# client.py : Have the a worker server fetch the content and check to see if has our
# advertising ID
#
# Syntax:
#  python3 client.py URL AdID SiteID -port 41000 -server 127.0.0.1 -tries 5 -gap 1
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

parsedArgs = argparse.ArgumentParser(description='Python client for confirming ad states')
parsedArgs.add_argument('URL', type=str, help='The URL to access', default='none')
parsedArgs.add_argument('AdID', type=str, help='The search string for our ads', default='none')
parsedArgs.add_argument('SiteID', type=str, help='The site ID to use for logging', default='XXX')
parsedArgs.add_argument('--port', type=int, help='Port for the server', default=54000)
parsedArgs.add_argument('--server', type=str, help='Hostname or IP address of server', default='127.0.0.1')
parsedArgs.add_argument('--tries', type=int, help='Number of times to check the site', default=1)
parsedArgs.add_argument('--gap', type=float, help='Gap between queries (in seconds)', default=1.0)
args = parsedArgs.parse_args()

# Note the current time


# Tally various results
numTests = 0
numTestsSuccess = 0
numTestsDetected = 0

for theTry in range(args.tries):
   # Note the current time

   numTests = numTests + 1

   # Protect against any relevant exceptions

   # Set up the socket

   # Connect to the remote server

   # Construct the string to send
   theRequest = "CHECK " + args.URL + " " + args.AdID + " " + args.SiteID

   # Send the string

   # Read the result string that is coming back

   # Wait (if needed) between scan requests

   # Note the completion time

   # Print the results

# Note the overall time and summarize the success / failures
