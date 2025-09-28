#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>
#include <sys/stat.h>
#include <stdbool.h>

#define MINPORTRANGE 54000
#define MAXPORTRANGE 54150
#define BACKLOG 10
#define MAX_REQUEST 1024
#define MAX_TOKENS 10

void sigchld_handler(int s) {
	(void)s; // quiet unused variable warning

	// waitpid() might overwrite errno, so we save and restore it:
	int saved_errno = errno;

	while(waitpid(-1, NULL, WNOHANG) > 0);

	errno = saved_errno;
}

// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa) {
	if (sa->sa_family == AF_INET) {
		return &(((struct sockaddr_in*)sa)->sin_addr);
	}

	return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

//once we get the check request parse to make sure the request is valid
int parse_check_request(int client_fd, char *url, char *adid, char *siteid) {
    char buffer[MAX_REQUEST];
    int bytes = recv(client_fd, buffer, sizeof(buffer)-1, 0);
    if (bytes <= 0) {
        // Connection closed or error
        return 0;
    }

    buffer[bytes] = '\0';

    // Tokenize the buffer
    char *tokens[MAX_TOKENS];
    int count = 0;
    char *token = strtok(buffer, " \r\n");
    while (token != NULL && count < MAX_TOKENS) {
        tokens[count++] = token;
        token = strtok(NULL, " \r\n");
    }

    // Validate CHECK command
    if (count != 4 || strcmp(tokens[0], "CHECK") != 0) {
        send(client_fd, "400 ERROR\n", 11, 0);
        return 0;
    }

    // Extract arguments, ALWAYS use strncpy because it is more secure than strcpy
    strncpy(url, tokens[1], MAX_REQUEST-1);
    url[MAX_REQUEST-1] = '\0';
    strncpy(adid, tokens[2], MAX_REQUEST-1);
    adid[MAX_REQUEST-1] = '\0';
    strncpy(siteid, tokens[3], MAX_REQUEST-1);
    siteid[MAX_REQUEST-1] = '\0';

    return 1;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        perror("ERROR: Enter only two parameters, the port number, and the directory location");
        exit(1);
    }

    char* portNumber = argv[1];

    if (atoi(portNumber) < MINPORTRANGE || atoi(portNumber) > MAXPORTRANGE) {
        fprintf(stderr, "ERROR: Port number needs to be between %d and %d (inclusive)\n", MINPORTRANGE, MAXPORTRANGE);
        exit(1);
    }

    char* directoryLocation = argv[2];

	// listen on sock_fd, new connection on new_fd
	int sockfd, new_fd;
	struct addrinfo hints, *servinfo, *p;
	struct sockaddr_storage their_addr; // connector's address info
	socklen_t sin_size;
	struct sigaction sa;
	int yes=1;
	char s[INET6_ADDRSTRLEN];
	int rv;

	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_flags = AI_PASSIVE; // use my IP

	if ((rv = getaddrinfo(NULL, portNumber, &hints, &servinfo)) != 0) {
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
		return 1;
	}

	// loop through all the results and bind to the first we can
	for(p = servinfo; p != NULL; p = p->ai_next) {
		if ((sockfd = socket(p->ai_family, p->ai_socktype,
				p->ai_protocol)) == -1) {
			perror("server: socket");
			continue;
		}

		if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes,
				sizeof(int)) == -1) {
			perror("setsockopt");
			exit(1);
		}

		if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
			close(sockfd);
			perror("server: bind");
			continue;
		}

		break;
	}

	freeaddrinfo(servinfo); // all done with this structure

	if (p == NULL)  {
		fprintf(stderr, "server: failed to bind\n");
		exit(1);
	}

	if (listen(sockfd, BACKLOG) == -1) {
		perror("listen");
		exit(1);
	}

	sa.sa_handler = sigchld_handler; // reap all dead processes
	sigemptyset(&sa.sa_mask);
	sa.sa_flags = SA_RESTART;
	if (sigaction(SIGCHLD, &sa, NULL) == -1) {
		perror("sigaction");
		exit(1);
	}

	printf("server: waiting for connections...\n");

	while(1) {  // main accept() loop
		sin_size = sizeof their_addr;
		new_fd = accept(sockfd, (struct sockaddr *)&their_addr,
				&sin_size);
		if (new_fd == -1) {
			perror("accept");
			continue;
		}

		inet_ntop(their_addr.ss_family,
			get_in_addr((struct sockaddr *)&their_addr),
			s, sizeof s);
		printf("server: got connection from %s\n", s);

		if (!fork()) { // this is the child process
			close(sockfd); // child doesn't need the listener

			//all received from the client once connected
			char url[MAX_REQUEST], adid[MAX_REQUEST], siteid[MAX_REQUEST];

			//something went wrong
			if (!parse_check_request(new_fd, url, adid, siteid)) {
				send(new_fd, "400 ERROR\n", 7, 0);
				close(new_fd);
				continue;  // go back to accept()
			}

			//getting host and pathname from url received
			char *host = NULL;
			char *path = NULL;

			char *p = strstr(url, "://");
			if (p) {
				*p = '\0';
				p += 3;
			} else {
				p = url;
			}

			host = p;
			//first instance of / for this
			char *slash = strchr(p, '/');
			if (slash) {
				*slash = '\0';
				path = slash + 1;
			} else {
				path = "";
			}

			struct addrinfo hints2, *res2, *q;
            int fetch_fd;

            memset(&hints2, 0, sizeof hints2);
            hints2.ai_family = AF_INET;
            hints2.ai_socktype = SOCK_STREAM;

			//Check to see if the hostname is valid
            if ((rv = getaddrinfo(host, "80", &hints2, &res2)) != 0) {
                fprintf(stderr, "400 ERROR getaddrinfo: %s\n", gai_strerror(rv));
                exit(1);
            }

            for (q = res2; q != NULL; q = q->ai_next) {
                fetch_fd = socket(q->ai_family, q->ai_socktype, q->ai_protocol);
                if (fetch_fd == -1) continue;

                if (connect(fetch_fd, q->ai_addr, q->ai_addrlen) == -1) {
                    close(fetch_fd);
                    continue;
                }
                break;
            }

            if (q == NULL) {
                fprintf(stderr, "failed to connect to remote host\n");
                exit(1);
            }

            char request[1024];
			//Finally send request to get html
			snprintf(request, sizeof(request),
                     "GET /%s HTTP/1.1\r\n"
                     "Host: %s\r\n"
                     "Connection: close\r\n\r\n", path, host);

            send(fetch_fd, request, strlen(request), 0);

			char msg[1024];
			snprintf(msg, sizeof(msg), "LOGDIR123123321321 %s\n", directoryLocation);
			send(new_fd, msg, strlen(msg), 0);

            char buffer[1024];
            int bytes;
			bool foundString = false;
            while ((bytes = recv(fetch_fd, buffer, sizeof(buffer), 0)) > 0) {
				if (strstr(buffer, adid)) {
					foundString = true;
				}

                send(new_fd, buffer, bytes, 0);
            }
			
			if (foundString) {
				printf("Found the string: %s in the file!\n", adid);
				send(new_fd, "200 YES\n", 8, 0);
			} else {
				printf("Could not find the string: %s in the file!\n", adid);
				send(new_fd, "200 NO\n", 7, 0);
			}

			close(fetch_fd);
			close(new_fd);
			freeaddrinfo(res2);
			exit(0);
		}

		close(new_fd);  // parent doesn't need this
	}

	return 0;
}