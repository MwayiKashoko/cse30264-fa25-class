# server.py : The server of sadness since our Java code was lost

import argparse
import os
import time
import socket

parsedArgs = argparse.ArgumentParser(description='Python server for confirming ad states')

parsedArgs.add_argument('--port', type=int, help='Port for the server', default=54000)
args = parsedArgs.parse_args()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
   # Coming at you live from any interface on the machine
   s.bind(('', args.port))

   s.listen()
   print(f"Server listening on {args.port}")

   while True:
      conn, addr = s.accept()
      with conn:
         print(f"Connected by {addr}")
         while True:
               data = conn.recv(1024)
               if not data:
                  break
               print(f"Received from client: {data.decode()}")
               conn.sendall(b"Hello from fake server!")