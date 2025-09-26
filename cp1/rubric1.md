# Rubric - Coding Project 1 - Part 1

25 points available in total

## General - 5 pts

* 1 pt - `README.md` is present in the `cp1` directory and contains group member information and any relevant virtual environment information (if Python is used)
   * Be sure to explicitly state any path / version constraints in your `README.md` if relevant
* 1 pt - Contributions are clearly identified for each group member
* 3 pts - No intervention is required for the TA (pathing changes, follow ups, etc.)
   * In short, the documentation should be clear and the TA should be able to run your code after a successful `make clean` and `make`

## Basic Operation - 8 pts

The basic operation will assume a default port of 54000 and access to the `file1.html` example (example with the ad string).

* 1 pt - Network connection is successfully established by the Python client
* 1 pt - Result is returned to the Python client
* 2 pt - Appropriate log sub-directory is created under `S1` with the correct date-time format
* 3 pts - Images are appropriately saved to a log directory
* 1 pt - Correct result string is returned

## Sequential Operation - 12 pts

The server will be exited and restarted.

* 1 pt - Exiting the server via Control-C and starting the server again does not cause an unhandled error
   * Note that you do not need to catch Control-C, only that your server starts back up again
* 3 pts - Correct operation if there are multiple retries (all to `file1.html`)
* 2 pts - Three different "sites" (S1, S2, S3)
* 4 pts - Varying sites with varying presence of ad string
* 1 pt - Ability to vary the server port
* 1 pt - Ability to change the search string
