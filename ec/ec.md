# Extra Credit - Packet Trains

The focus of this extra credit is to create a set of tools that allows for the construction of well-formed packet with specific timing sequences, e.g. packet trains.  Your task is to build a basic client and server that realizes the targeted functionality described below.

As this is an extra credit assignment, various aspects may not be fully defined.  Feel free to ask questions.  This extra credit assignment should be done individually and may be worth up to 10 points.

## Sub-Directories

The following sub-directories should be contained within the submitted .tar.gz file.

* ecpt - Base Directory that we will use for testing / various concepts
* ecpt / server / python
* ecpt / client / python

## Rationale

For our various sets of WiFi testing (and to some extent cellular), our research group needs the ability to be able to inject particular timing waveforms.  Previously, we had code via ScaleBox and FMNC that would ride on top of TCP.  We needed TCP specifically because we wanted to be able to deploy to mobile nodes as well as to conduct various live demos (e.g. make a web get / operate within the web get).

The goal is to get back there eventually but in the short term, we need ways to be able to deliver controlled packet sending whereby we can control the bursts, size, and timing of the various packets.

To that end, you will be building up a UDP solution whereby a client can send requests to generate various packet sequences (aka a packet train).  However, we do need to prototype and figure out how exactly we should format said requests, the extent to which we can accurately control the resulting sequences, and how we keep the overall system itself reasonably secure and safe from malicious usage.

The focus will be to build up the a prototype named _simpleshimmy_.  The name shimmy comes from the shimmy that a dog does to dry off and given that this is a UDP-focused version, it is dubbed simpleshimmy.

## System Properties

The system will have the following characteristics:

* A client will connect to the server, possibly presenting some sort of credentials or authorization.
   * For this extra credit, you should restrict request to only be allowed from campus.
   * Explore how you might use some sort of cryptography mechanism (ex. HMAC) where the client has a secret and the server has the appropriate information also stored.
* The client will make a request to the server for the desired packet timing sequence(s) whereby the sequence encoding length is minimized so as to afford containment within a single packet.
   * For the purpose of the extra credit assignment, think of it as picking from a menu of timing sequences (packet train sequence number 3) that are defined at the server via set of JSON files.
   * The client will also provide an identifier to use for the timing sequence.
* The packet sequence or packet train represents a set of packets that will be sent by the server to the client.
   * A packet train consists of a series of packets.  Each packet is a particular length (ideally less than MTU) with a specified time gap between each packet.  Packets may be sent in bursts (no time between packets).
   * Packet trains may be repeated and packet lengths and gaps may vary with all packets in the train.
   * A train may be set to be sent after a small delay or at a specific wall clock time (start of packets).
   * Packets when sent should contain appropriate identifiers with respect to which packet in the sequence that the packet is associated with.  Such information should occur as early in the payload as possible.
* The server will transmit the packet train as requested by the client using the established UDP socket.
* The client should create a set of output files that adequately captures when each individual packet was received and the order that said packet was received in.
* The server should also create a set of output files that adequately captures when the packets were sent.

You may write the code in either Python or C but Python is generally recommended.

## Basic Packet Sequences

You should be able to support the following configurations.

* Send 10 packets each of 1000 bytes with a gap of 10 milliseconds between
* Send 50 packets each of 250 bytes with a gap of 1 millisecond between
* Send 5 packets of 1000 bytes, 10 ms gap, 5 packets of 1100 bytes, 10 ms gap
* Send 3 packets of 1000 bytes with no gap (burst), 30 ms gap, 3 packets of 1000 bytes with no gap

It is up to you how to encode the configuration as a JSON file.  Your server should have a default sub-directory that it reads for the various configurations (ex. configs).  Remember, each packet in the sequence should have a monotonically increasing identifier (1, 2, 3, etc.).

## Client Logging

Your client should create a log file in a format of your choosing to properly record when various packets are received.  The client should only output to confirm a successful setup with the server for the sequence and then confirm the number of packets that were received.

You may elect to create either a CSV (ideal) or a JSON that should contain the time the packets were received, the ID of the packet, the size of the packet, and the gap from the last received packet.

## Client / Server Configuration

You should define various options / arguments for the client and server.  Specifically, your code should be able to specify the port that should be used. You may define the other arguments as you see fit.

## Initial Testing

The server can be tested initially using localhost.  Once the client seems to be robust, the CSE student machines can be used for testing.

## Operational Confirmation

For each of the respective configurations, confirm that the timing sequence seems appropriate both when executed on localhost as well as executed when the server is run on the CSE student machine.

## Submission

Submit a complete writeup via a README.md file describing your solution and the set of respective features that you have implemented.  Include a set of log files for each of the configurations. Submit your code as a .tar.gz file.

* The base code is worth up to 8 points.
* Support for an authentication / authorization mechanism is worth up to 2 points. You may elect to only do the authorization portion for 2 points.
