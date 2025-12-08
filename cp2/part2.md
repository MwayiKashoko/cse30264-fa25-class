# Coding Project 2 - Part 2

Google Drive Link: See Canvas for Part 1 or Part 2

## General Overview

In Part 1, we wrote the back end for the server, some testing tools, and did both "good" and "bad" packet captures.  In Part 2, we are going to do a bit more lifting on the tool side, examining how we can use existing system tools / libraries for the purposes of boutique tools which can quite frequently be the case when deadling with unique network stacks.  Wireshark can be lovely for high level analytics (what is going on) but it often struggles when trying to dive deeper.

## Step 0 - Fetch the Captures

Make sure you have access to your respective captures from Part 1 as well as a few captures from other teams.  The captures do not need to be part of your repository due to their size and you should appropriately use `.gitignore` as needed.

## [15 pts] Step 1 - Boutique Tools

For the first step of Part 2, you will be crafting several boutique or what some might refer to as bespoke tools, tools specifically geared at the captures that we gathered during the first part.  While one could argue that much of your undergraduate degree consists of these kinds of tools, your task with Step 1 is to adddress a few of the minor nits / difficulties for prepping for the analytical parts of Step 2.

All code for Step 1 should go into a `tools` subdirectory off of `cp2`.

You may use any tools present on the CSE student machines to help you accomplish Step 1 (system tools, Python code, shell scripts, etc.).

* Step 1a: `find-client`, `find-server`
* Step 1b: `focus-filter`
* Step 1c: `find-tcp-max`, `pto`
* Step 1d: `packet-smash`

You will have a healthy amount of discretion on the exact arguments.  Make sure to document things appropriately in your README.

### Step 1a - Identify the Client and Server

Write two bits of code to extract either the IP address associated with the client or with the server for the test.  These pieces of code should take in a packet capture file (.pcap) and output the IP address of client (`find-client`) or server (`find-server`).

```
%./find-client this-capture.pcap
10.5.3.190
%./find-server this-capture.pcap
129.74.120.75
```

Remember that you have a few pieces of information that can be helpful.  You know that the capture was done from the perspective of the client.  You also know the rough port range where the server should be operating. You also know there will be multiple connections to the server.

### Step 1b - Apply the Filter

Write a tool (`focus-filter`) that reduces the packet capture to only the relevant packets for the purposes of the capture (only the client and the server).  Use your tool that you wrote in Step 1a to help you accomplish this task.

### Step 1c - Prune to the Max

As many of you noticed, the packet captures were fairly large once ten iterations were put together of downloading the 18MB+ JSON.  Since we are conducting analytics, the payload itself is largely irrelevant to what we would like to accomplish.  Your next task is to write two tools: `find-tcp-max` that scans a packet capture to determine the minimum packet length that would capture the entirety of the Layer 2, Layer 3, and Layer 4 packet headers (inclusive of TCP options), and `pto` (prune TCP only) that converts a packet capture into only its minimal data as needed (Layers 2-4).

Hint: The `tcpdump` tool can be run with various arguments and may be quite useful.

A few notes:

* The `pto` script will likely need to call `find-tcp-max` to determine the minimum packet length.
* It is OK if some packets have part of the payload.  The key is not to miss any TCP option information.
* Your output file should be the same name of the file with `pto-` prepended to the file name, e.g. `this-capture.pcap` would become `pto-this-capture.pcap`.

### Step 1d - Smash Those Packets

Finally, once we have largely reduced the size of the packets, the next task is to compress the data.  Write a script named `packet-smash` that takes in a directory as an input of packet captures, runs all of your various optimizations above, and then puts all of the content into a single `.tar.gz` file that is labeled `smash.tar.gz` and the location specified as the second argument.

Report as part of your output the original size of the various packet captures and then the resulting size.

* You may assume that packet captures must end with `.pcap`
* Only valid packet capture files need to be considered for reporting purposes
* You should report at least: number of captures, cumulative size of the captures, final size of the resulting archive, percent reduction from your tool
* You do not need to traverse sub-directories

## [20 pts] Step 2 - Advanced Analytics

With the housekeeping from Part 1 in place, the next task is to write several analytical tools to help with answering the questions from Part 3.  We know the respective performance times from your client that you wrote in Part 1, now we want to dive a bit deeper into the why.

For the purposes of Step 2, you can assume that you will have a directory specified as an input of various packet captures.  Those packet captures will not be placed `good` or `bad` subdirectories but will simply exist as a collection of `.pcap` files and `.txt` files (text files were metadata / information).  All text files will have the same name as the `.pcap` file associated with the capture.

For this part, you should start with your captured data and then move onto using your "cleaned up" data from Part 1 (not in the archive, just cleaned up).  Once you feel confident, add in a few cleaned up files from other groups.  You are welcome to leave the naming of the files containing either `good` or `bad`.

The code for Step 2 should go in the `analytics` subdirectory off of `cp2`.

### Step 2a - Worst Performers

We are interested in two types of perfomers with regards to poor performance for Step 2a keying off of the number of TCP retransmissions associated with any download on the basis of a given host as well as a given access point (AP).

Write a script / code named `analyze-perf` that does the following:

* Take in a directory that contains `.pcap` files
* Process all of the `.pcap` files identifying:
   * The number of TCP retransmissions on a per-flow basis for only the data downloads (e.g. the bigger downloads of the JSON information)
   * The information grouped on a capture by capture basis (single `.pcap` file)
   * The captures grouped on the basis of host and access point
* Compute statistics for TCP retransmissions across a given capture including minimum, maximum, mean, and median on both a capture basis node basis (host, ap)
* Report basic information about each of the input files and the number of observed packets
* Provide a sorted list of the number of tests for each host and access point (e.g. host X had Y tests)
* Report a sorted list on the basis of hosts and access points for the poorest performance in a tabular format (human readable) that lists the MAC address, number of tests, and the various statistics

### Step 2b - Extract Analysis

Create an output of your code under the following scenarios using the following names in the `analytics` sub-directory:

* **self.txt**: A run of your tool on your packet captures from Part 1
* **self-plus.txt**: A run of your tool on a total of four packet captures from Part 1
* **self-big.txt**: A run of your tool on at least ten packet captures from Part 1

## [10 pts] Step 3 - Do the Analytics

For Step 3, use your tool to answer the following questions in a file named `insight.txt` in the `cp2` directory.

* Do the `good` packet captures have any TCP retransmissions?  Should they have retransmissions? Why or why not?
* What is the worst performing host and worst performing access point when considering at least 10 different captures?  What makes it worse? Was your `bad` capture from Part 1 better or worse?
* Are any of the captures so bad as to be non-functional (in terms of a client using the server)?  Why or why not?
* Drawing more broadly and from beyond your tools, how does the latency to the CSE student machine compare to the cloud? Does that play a role in what you observed from a performance perspective? Why or why not?

## Extra Credit

There are a few opportunities to earn extra credit as noted below.  Extra credit must be submitted by the normal due date to be considered.

* [1.5 pts] Write your tool in Step 2 to take in either a sub-directory (default) or to be able to take in a smashed packet archive (created in Step 1).
* [1 pt] Write your tool from Step 1 to allow for the traversal of subdirectories with special care taken to avoid following any symlinks
* [1 pt] Write your tool in Step 2 to allow following sub-directories (avoiding symlinks)
* [3 pts] Write your tool to compute the change in RTT from the start of a given data download until the end of the data download

## Submission

* Use the subdirectory named `cp2` in the repository for your group
* Create a `README-part2.md` identifying the contributions from each member of the group.
   * Note that each member of the group should have at least one substantial commit.
   * The `README-part2.md` file should also contain the virtual environment packages that are required.
* Create a `README.md` file inside of each subdirectory for the tools from Part 2 containing instructions on how to run the code
* Push your code to Github and submit the full hash of your submission via Canvas. Note that only one member needs to submit the hash.