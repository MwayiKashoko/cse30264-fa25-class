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
#include <sys/stat.h>
#include <stdbool.h>

#define MINPORTRANGE 54000
#define MAXPORTRANGE 54150
#define MAX_REQUEST 1024
#define MAX_TOKENS 10

// Get sockaddr, IPv4 or IPv6
void *get_in_addr(struct sockaddr *sa) {
    if (sa->sa_family == AF_INET)
        return &(((struct sockaddr_in*)sa)->sin_addr);
    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

// Parse CHECK request from buffer
int parse_check_request(char *buffer, char *url, char *adid, char *siteid) {
    char *tokens[MAX_TOKENS];
    int count = 0;
    char *token = strtok(buffer, " \r\n");
    while (token != NULL && count < MAX_TOKENS) {
        tokens[count++] = token;
        token = strtok(NULL, " \r\n");
    }

    if (count != 4 || strcmp(tokens[0], "CHECK") != 0)
        return 0;

    strncpy(url, tokens[1], MAX_REQUEST-1);
    url[MAX_REQUEST-1] = '\0';
    strncpy(adid, tokens[2], MAX_REQUEST-1);
    adid[MAX_REQUEST-1] = '\0';
    strncpy(siteid, tokens[3], MAX_REQUEST-1);
    siteid[MAX_REQUEST-1] = '\0';

    return 1;
}

int main(int argc, char **argv) {
    if (argc != 7) {
        fprintf(stderr, "Usage: %s <server_port> <log_dir> <server_ip> <orchestrator_ip> <orchestrator_port> <server_id>\n", argv[0]);
        exit(1);
    }

    char* portNumber = argv[1];
    char* directoryLocation = argv[2];
    char* orchestrator_ip = argv[4];
    char* orchestrator_port = argv[5];

    if (atoi(portNumber) < MINPORTRANGE || atoi(portNumber) > MAXPORTRANGE) {
        fprintf(stderr, "ERROR: Port must be between %d and %d\n", MINPORTRANGE, MAXPORTRANGE);
        exit(1);
    }

    int sockfd;
    struct addrinfo hints, *servinfo, *p;
    int rv;
    int yes = 1;

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_flags = AI_PASSIVE;

    if ((rv = getaddrinfo(NULL, portNumber, &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 1;
    }

    // Bind UDP socket
    for (p = servinfo; p != NULL; p = p->ai_next) {
        if ((sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
            perror("socket");
            continue;
        }
        if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1) {
            perror("setsockopt");
            exit(1);
        }
        if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
            close(sockfd);
            perror("bind");
            continue;
        }
        break;
    }

    freeaddrinfo(servinfo);
    if (p == NULL) {
        fprintf(stderr, "Failed to bind socket\n");
        exit(1);
    }

    printf("Worker UDP server listening on port %s...\n", portNumber);

    // Prepare orchestrator address info
    struct addrinfo hints_orch, *orchinfo;
    memset(&hints_orch, 0, sizeof hints_orch);
    hints_orch.ai_family = AF_INET;
    hints_orch.ai_socktype = SOCK_DGRAM;

    if ((rv = getaddrinfo(orchestrator_ip, orchestrator_port, &hints_orch, &orchinfo)) != 0) {
        fprintf(stderr, "Orchestrator getaddrinfo: %s\n", gai_strerror(rv));
        exit(1);
    }

    while (1) {
        struct sockaddr_storage client_addr;
        socklen_t addr_len = sizeof client_addr;
        char buffer[MAX_REQUEST];

        int bytes = recvfrom(sockfd, buffer, sizeof(buffer)-1, 0, (struct sockaddr *)&client_addr, &addr_len);
        if (bytes == -1) {
            perror("recvfrom");
            continue;
        }
        buffer[bytes] = '\0';

        char s[INET6_ADDRSTRLEN];
        inet_ntop(client_addr.ss_family, get_in_addr((struct sockaddr *)&client_addr), s, sizeof s);
        printf("Received packet from %s\n", s);

        char url[MAX_REQUEST], adid[MAX_REQUEST], siteid[MAX_REQUEST];
        if (!parse_check_request(buffer, url, adid, siteid)) {
            const char *err = "400 ERROR\n";
            sendto(sockfd, err, strlen(err), 0, (struct sockaddr *)&client_addr, addr_len);
            continue;
        }

        // Parse host/path
        char *host = NULL, *path = NULL;
        char *p2 = strstr(url, "://");
        if (p2) { *p2 = '\0'; p2 += 3; } else { p2 = url; }
        host = p2;
        char *slash = strchr(p2, '/');
        if (slash) { *slash = '\0'; path = slash + 1; } else { path = ""; }

        // Connect to remote host (TCP)
        struct addrinfo hints2, *res2, *q;
        int fetch_fd;
        memset(&hints2, 0, sizeof hints2);
        hints2.ai_family = AF_INET;
        hints2.ai_socktype = SOCK_STREAM;

        if ((rv = getaddrinfo(host, "80", &hints2, &res2)) != 0) {
            fprintf(stderr, "400 ERROR getaddrinfo: %s\n", gai_strerror(rv));
            const char *err = "400 ERROR\n";
            sendto(sockfd, err, strlen(err), 0, (struct sockaddr *)&client_addr, addr_len);
            continue;
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
            fprintf(stderr, "Failed to connect to remote host\n");
            const char *err = "400 ERROR\n";
            sendto(sockfd, err, strlen(err), 0, (struct sockaddr *)&client_addr, addr_len);
            freeaddrinfo(res2);
            continue;
        }

        char request[1024];
        snprintf(request, sizeof(request),
                 "GET /%s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n",
                 path, host);
        send(fetch_fd, request, strlen(request), 0);

        // Check response for adid
        char resp_buffer[1024];
        int n;
        bool found = false;
        while ((n = recv(fetch_fd, resp_buffer, sizeof(resp_buffer)-1, 0)) > 0) {
            resp_buffer[n] = '\0';
            if (strstr(resp_buffer, adid))
                found = true;
        }

        char final_response[2048];
        if (found) {
            printf("Found the string: %s in the file!\n", adid);
            snprintf(final_response, sizeof(final_response),
                     "LOGDIR123123321321 %s\n200 YES\n", directoryLocation);
        } else {
            printf("String %s not found in the file!\n", adid);
            snprintf(final_response, sizeof(final_response),
                     "LOGDIR123123321321 %s\n200 NO\n", directoryLocation);
        }

        // Send final response to orchestrator, not client
        sendto(sockfd, final_response, strlen(final_response), 0,
               orchinfo->ai_addr, orchinfo->ai_addrlen);

        close(fetch_fd);
        freeaddrinfo(res2);
    }

    close(sockfd);
    freeaddrinfo(orchinfo);
    return 0;
}