#!/usr/bin/env python3

"""
Author: Luke Zeman
File: echo_server.py
Description: Simple TCP server that listens for incoming connections and prints received data.
Course: CSC 346 - Cloud Computing
Date: March 2025
"""

from socket import *

def main():
    server_sock = socket()
    server_addr = ("0.0.0.0", 9999)
    server_sock.bind(server_addr)

    server_sock.listen(5)
    print(f"Server listening on port {server_addr[1]}...")

    try:
        while True:
            conn_sock, conn_addr = server_sock.accept()
            print(f"Accepted connection from {conn_addr}")

            data = conn_sock.recv(9999).decode()
            print(f"Received data:\n{data}")

            conn_sock.close()
            print("Connection closed.\n")
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_sock.close()

main()