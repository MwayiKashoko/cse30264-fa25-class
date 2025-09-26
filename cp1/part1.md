# Coding Project 1

## General Overview

The goal of the project is to get you experience with both TCP and UDP, blending a bit of C / C++ (the code you will be writing) with a Python client (provided to you). The project may be completed in a group of up to four students and has two parts: (1) Basic operation including the TCP server portion of the code and (2) Optimizations and incorporation of a UDP logging function.

## Task Overview

The company that you are working for has recently embarked upon digital advertising across a variety of platforms.  Part of that effort involves confirming that the ads for the company do not appear next to controversial content.  You are working within a team and have been given a design blueprint created by the senior architect.  Specifically, the architect has noted that the past Java code (which was lost in a catastrophic backup issue) was too slow and the architect would like to create a newer / faster C or C++ version. The old and possibly buggy Python prototype code did get preserved.

## Data Pipeline

The tool works in the following manner:

1. A Python client takes in a site to scan, the advertising string to search for, and an ID to record for the site when logging
2. The client makes a request to the server asking the server to fetch a specific site.
3. The server fetches the content for the site.
4. After fetching the site content, the server searches the content for any references of the noted advertising string.
5. If the string is found, any images are retrieved from the website from the content and saved to a local directory as a log.
7. The results are returned back via the HTTP-like protocol to the client that displays the result to the console.
8. As appropriate, the client will repeat the process to get a certain number of retrievals or to check multiple sites.

The protocol syntax is as follows:

```
CHECK http://ns-mn1.cse.nd.edu/cse30264/ads/file1.html IRISH_CSE S1
```

where the site `http://ns-mn1.cse.nd.edu/cse30264/ads/file1.html` is requested to be checked for the advertising string `IRISH_CSE`. If that advertising string is found, the server should scan the content of the webpage for any `IMG` strings and then retrieve the image associated with any of the strings.  It should save each of the images to a local subdirectory per the appropriate structure.  Otherwise, it should simple create an empty directory.

Your server code will need to do the following:

* It should take in two arguments, the port number of listen on (first argument) and the log directory location (second argument).
* Listen for new connections on a particular port from 54000-54150
   * You should not start the server if the port number does not fall in that range.
   * These ports are set up for the networking class.  You can nominally pick anything randomly in between or coordinate with other groups via Slack.  For this part of the project, you will only need one port for the server.
   * The socket will be a TCP socket (aka SOCK_STREAM)
* Once the connection is made, look for the connection / request string as noted above.  You may assume for the purposes of Part 1 that all strings will be well-formatted.
   * You should confirm that the CHECK command is requested and that a correct number of arguments are present.  If there is an insufficient number of arguments or too many arguments are present, you should return the 400 ERROR.
* Fetch the content as you see fit from the specified website.
   * You are welcome to fork a child process or any other mechanism as you see fit (e.g. have your code fork and exec to run a `curl`).  Or you could invoke your own Python code.
   * The only rule per se is that the server has to at least be in C or C++ for accepting the connection and it has to run on the student machine with an appropriate Makefile.
* Analyze the content for an image references.  You can key off of the `<IMG` string (uppercase or lowercase).  If there is an image reference, you should then fetch any of the URLs reference inside of the image reference.
   * Look up how images are specified in HTML to figure out the syntax.
   * You may want to use a wide variety of tools to help with both identifying the reference as well as the URL.
   * It may be helpful to create a temporary directory for staging and downloading content.
* All images should be downloaded to a local directory that follows the structures of `logs\SiteID\date-time` where the `logs` directory was specified as a startup argument, the date is the date in the syntax of `YYYY-MM-DD` with Y=year, M-month, D=day with zero padding being included.  The time field is `HH-mm-SS` where H=Hour, m=Minute, and S=Seconds, also zero padded.  The SiteID is drawn from the initial request and should be set by the client.
   * You may assume for Part 1 that the SiteID is set correctly by the client.
   * You may assume that the minimum gap between any requests is spaced by at least one second.
   * It is up to you how best to capture the time and when would be appropriate to do so.
   * You may also presume that all images will be uniquely named.
   * The site ID sub-directory may exist.  If not, you should create it.
   * The date-time format will end up being `YYYY-MM-DD-HH-mm-SS` altogether.
* The returned result code can be one of three results:
   * 200 YES SiteID date-time - This means that there was content found with the advertising string and that images were logged. The SiteID is listed as well as the date-time string (this should match with the directory that was created).
   * 200 NO - This means that there was no content found with the advertising string.  No images should be logged.
   * 400 ERROR - An error occurred (web server did not respond, content not found, etc.).  It is up to you how / if you would like to explain the error.
   * This response message should be only a single line.
* There is no need to write the part that checks or compares the images.  That part of the code still "works" but is not your responsibility.

## Operation

As noted above, you have a fair amount of latitude with respect to how the "guts" of your server (the worker) will operate.  Effectively, you can think of your server as being a worker that sits and waits for instructions from the client.

## Submission

* Create a sub-directory named `cp1` in your repository.
* Create a `README.md` file inside of `cp1` containing instructions on how to run your code as well as identifying the contributions from each member of the group.   There should be at least one `Makefile` to compile your C or C++ code.
   * Note that each member of the group should have at least one substantial commit.
* Push your code to Github and submit the full hash of your submission via Canvas. Note that only one member needs to submit the hash.

## Rubric

25 points in total in the Coding Project 1 category

[Rubric](./rubric1.md)

## Looking Ahead

In Part 2, we will add in a high level dispatcher and various optimizations to the code to help it run faster.
