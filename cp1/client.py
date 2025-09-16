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
# -port   Optionally changes the port from 54000 to a specific value
# -server The IP or hostname of the server, default is localhost
# -tries  The number of times to fetch this site from the server (default is one)
# -gap    The gap between tries (default is 1 second)
#
