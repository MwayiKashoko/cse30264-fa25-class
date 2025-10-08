# Rubric - Coding Project 1 - Part 2

35 points available in total

## General - 5 pts

* 1 pt - `README.md` is present in the `cp1-part2` directory and contains group member information and any relevant virtual environment information (if Python is used)
   * Be sure to explicitly state any path / version constraints in your `README.md` if relevant
* 1 pt - Contributions are clearly identified for each group member
* 3 pts - No intervention is required for the TA (pathing changes, follow ups, etc.)
   * In short, the documentation should be clear and the TA should be able to run your code following the update

## Basic Operation - Single Worker - 6 pts

The basic operation will assume a default port of 54000 (for the orchestrator) and access to the `file1.html` example (example with the ad string). A single worker will be created for processing (ideally via `launch-workers`).  Three requests will be made.

* 1 pt - Network request is successfully made to the orchestrator with appropriate output
* 1 pt - Result is checkable / correct via the `check-hits` script
* 2 pt - Appropriate log sub-directory is created under `S1` with the correct date-time format
* 2 pts - Images are appropriately saved to the log directory

## Basic Operation - Two Workers - 6 pts

Same setup as the previous example but now with two workers both running on the same machine. Three requests will be made.

* 1 pt - Network connection is successfully established by the Python client
* 1 pt - Result is checkable / correct via the `check-hits` script
* 2 pt - Appropriate log sub-directory is created under `S1` with the correct date-time format
* 2 pts - Images are appropriately saved to the log directory

## Variations - Workers and Tasks - 10 pts

Variations involving the invocation of various fetches / etc.

* 2 pts - All five sites via two workers
* 2 pts - Enqueuing 10 requests rapidly
* 2 pts - One worker on one student machine, the other worker on a different student machine from the orchestrator
* 2 pts - Variations with multiple workers (3, 4, 5)
* 2 pts - Variations on the orchestrator port setting

## Features / Documentation - 8 pts

* 5 pts - Correct operation, and testing of features introduced by each group member
* 3 pts - Documentation and invocation of features
