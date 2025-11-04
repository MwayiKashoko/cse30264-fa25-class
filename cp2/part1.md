# Coding Project 2 - Part 1

## General Overview

With Coding Project 1, we gained a healthy amount of experience programming with C / C++ as well as Python, examining TCP and UDP socket programming.  In this project, we are will eschew the "hard" parts of socket programming and instead go to a more traditional approach, namely that of a REST-like API by leveraging Python on the Flask on the back end and then capturing / analyzing the performance using Wireshark.  Part 1 will focus on the data capture elements while Part 2 will focus on the analytics of the data that you will capture.

## Task Overview

The goal of Part 1 is to accomplish three tasks:

* Write a [Flask](https://flask.palletsprojects.com/en/stable/) in Python to serve up data via a REST-like API (data blobs, analyzed data blobs).  This code will run on the CSE student machines in the port ranges that we used in the first coding project.
* Automate and measure the performance of your Flask server using the [requests](https://pypi.org/project/requests/) library
* Capture two reference examples of data running your automation script

## Python Flask + REST

[Flask](https://flask.palletsprojects.com/en/stable/) is a lightweight Python library (technically a framework) that provides a WSGI (Web Server Gateway Interface). Basically, it provides a framework where you can invoke Python code in response to various web requests to dynamically generate content. In contrast to a static web page or even a page with embedded CSS and scripts, think of Flask as a server that provides the responses to a remote web client.  In the past, such interfaces might have been done with say an Apache server coupled with PHP or Perl. More modern variants use a wide variety of approaches but for this class, we are interested in something relatively lightweight and that we can run on the student machines.

```
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```

Unlike a normal Python script, there are some subtle nuances to Flask.  You will want to read up on the [Flask tutorial](https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application) but essentially, it boils down to this: you register what can loosely be akin to callbacks on particular URLs where a function invocation is _routed_ based off of the path specified by the URL after the hostname.  This allows you to encode behaviors on the basis of the path such as `data/json` gives us the data in a JSON format while `data/csv` might give us data as a CSV.  The pathing and how you handle it in the code is entirely up to you.

For our REST server, we are going to do three things: (1) Serve up JSON; (2) Be able to apply a filter via parameters; (3) Compute a transformed result and provide it as a JSON

* Your code should have two variables that are well defined and accessible:
   * The port number to use
   * A list that contains the specific data file or files that should be considered when serving data
      * You may presume that the file location is relative to where your script is located (e.g. `data/set1/data-all.json`)
* The data should be served up via the `/data` path and should have the ability to specific the month (m), day (d), and year (y) as parameters (e.g. m=4&d=4&y=2024) as well as the direction (dir) and interface (if). The returned data should be a JSON.  If the result is empty (nothing matches), it should be an empty JSON.
   * If a parameter is not specified, nothing should be filtered on the basis of that parameter.
   * Only iperf tests should be considered.
* There should be two other endpoints supported off of `/dl/stat` which includes `mean` and `peak`  to compute the daily mean values on any day where there is at least one speed test in the download direction (any interface) as well as the peak or maximum observed download speed (from the `tput_mbps` field).

Example files can be found in the `data` sub-directory in the class repository.  A brief explanation of the data is described below (see the `data-10.json` example).

* The files contain a list of speed tests conducted over a multi-month period at two different locations using a measurement tool called iperf.
* Each JSON file contains a timestamp of when the speed test data was gathered.  The timestamp contains the month, day, year, and hour, minute, and seconds.
* The direction and interface fields denote the direction of the test and the specific interface used for the test.
* For the speed, we will use the `tput_mbps` field.
* The [segment-json.py](./help/segment-json.py) may be helpful to refresh your memory about Python and filtering.

Run your server on the CSE student machine and use a web browser on your laptop to confirm that the code is running correctly.  Note that some of the files are fairly small while others are much larger.

## Automated Testing

Write a Python script using the `requests` library to time all three endpoints at least fifteen times (data, mean, peak).  Use an appropriate approach for statistics to compute the minimum, maximum, mean, median, and standard deviation.  Report those values as part of your output as run on your laptop to accompany your capture (see next subsection).  Note that you will need to be on campus for that testing.

## Capture

Using Wireshark, do a packet capture while running your script in two different locations:

* The first location should be one with good signal strength / good performance
* The second location should be one with less then excellent performance

You can confirm the performance by running either Ookla Speedtest or the CloudFlare Internet Speed Test before conducting your capture.  Try not to do anything else during your test and use the same laptop for each of the tests.

For the data endpoint, use the `data-all.json` file without any filtering.  For the `mean` and `peak` endpoints, filter for May 2024 and wlan0 in the downlink direction.

Using the filter tools for Wireshark, create pcap that contains only the connections to and from your Flask server (e.g. filter for a specific TCP port and IP address). You can do that either by setting the filter prior to your capture or after your capture.

Place the captures in the `capture` sub-directory in your `cp2` repository.  Name the files `good.pcap` and `poor.pcap` to help identify the captures.  Make sure to save your results of your testing script output as `good.txt` and `bad.txt`.

We will be pooling different pcaps from the class for the second part of the project.

## Submission

* Create a sub-directory named `cp2` in the repository for your group
   * If your group or repository is changing, please let the TA and instructor know ASAP
* Create a `README.md` file inside of `cp2` containing instructions on how to run your code as well as identifying the contributions from each member of the group.
   * Note that each member of the group should have at least one substantial commit.
   * The `README.md` file should also contain the virtual environment packages that are required.
* Create an `info.md` file in the `capture` sub-directory that contains information about the captures (where, when)
   * Include in the `capture` directory the output of your automation scripts as noted above
* Push your code to Github and submit the full hash of your submission via Canvas. Note that only one member needs to submit the hash.

## Rubric

35 points in total in the Coding Project 2 category
