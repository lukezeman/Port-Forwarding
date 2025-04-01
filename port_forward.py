#! /usr/bin/python3

"""
Author: Luke Zeman
File: port_forward.py
Description: Forwards TCP traffic between a client and server using sockets and threading.
Course: CSC 346 - Cloud Computing
Date: March 2025
"""

from socket import *
import sys
import threading
import random

def read_server_location(location):
    """
    Parses the provided location string into an IP and port number.

    Parameters:
        location (str): A string in the form 'ip:port'

    Returns:
        tuple: (ip (str), port (int))
    """
    ip = "0.0.0.0"
    port = random.randint(1024, 65535)

    if location != ":" and location != "":
        location = location.split(":")

        if location[0] != "":
            ip = location[0]
        
        if location[1] != "":
            port = int(location[1])

    return ip, port

def worker(source, destination):
    """
    Forwards data between a source and destination socket.

    Parameters:
        source (socket): Source socket to read from.
        destination (socket): Destination socket to send to.

    Returns:
        None
    """
    while True:
        try:
            data = source.recv(4096)
        except Exception as e:
            print(f"Exception during recv: {e}")
            break
        # No more data left to send.
        if data.strip() == b"":
            print("No more data received. Shutting down connection.")
            destination.shutdown(SHUT_WR)
            break
        print(f"Forwarding data: {data}")
        try:
            # Send data to the other end.
            destination.sendall(data)
        except Exception as e:
            print(f"Exception during sendall: {e}")
            break
        print("Data sent to destination.")

    try:
        source.close()
    except Exception as e:
        print(f"Exception during source close: {e}")
    try:
        destination.close()
    except Exception as e:
        print(f"Exception during destination close: {e}")

def port_forward(cli_sock, dest_host, dest_port):
    """
    Connects to the destination server and starts forwarding traffic
    between the client and server using two threads.

    Parameters:
        cli_sock (socket): Client's socket connection
        dest_host (str): Destination host IP
        dest_port (int): Destination port

    Returns:
        None
    """
    serv_sock = socket()
    serv_sock.connect((dest_host, dest_port))
    print(f"Connected to server on port {dest_port}")

    # Start bi-directional forwarding between client and server.
    cli_serv = threading.Thread(target=worker, args=(cli_sock, serv_sock))
    serv_cli = threading.Thread(target=worker, args=(serv_sock, cli_sock))

    cli_serv.start()
    serv_cli.start()

def main():
    if len(sys.argv) == 3:
        # Custom bind IP and port for incoming connections.
        server_location = sys.argv[1]
        destination = sys.argv[2]
        
        serv_ip, serv_port = read_server_location(server_location)
       
        destination = destination.split(":")
        dest_host = destination[0]
        dest_port = int(destination[1])

    if len(sys.argv) == 2:
        # Random port and default IP if only destination is given.
        destination = sys.argv[1]
        destination = destination.split(":")
        dest_host = destination[0]
        dest_port = int(destination[1])

        serv_ip = "0.0.0.0"
        serv_port = random.randint(1024, 65535)

    list_sock = socket()
    list_sock.bind((serv_ip, serv_port))
    list_sock.listen(5)
    print(f"Listening on port {serv_port}...")

    while True:
        cli_sock, addr = list_sock.accept()
        print(f"Accepted connection from {addr}")
        # Start a new thread to handle the connection.
        threading.Thread(target=port_forward, args=(cli_sock, dest_host, dest_port)).start()

main()
