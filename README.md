# Port-Forwarding
This project includes a simple Python-based TCP port forwarder and a minimal test server. It was developed for a cloud computing course to demonstrate how network traffic can be routed through a proxy using low-level socket programming and threading.

# Files Included
- port_forward.py
  - Forwards TCP traffic between a client and a destination server. Supports multiple simultaneous connections using threads.
- open_server.py
  - A simple TCP server that listens on a port, prints received data, and then closes the connection.

# How To Run
1. Start the Test Server (default port 9999)
  - python3 open_server.py
2. Run the Port Forwarder
  - python3 port_forward.py :9999 127.0.0.1:9999
3. Send Test Traffic
  - curl --data "Test" http://127.0.0.1:<forwarded_port>

# Learning Objectives
- Understand how socket communication works between client and server
- Practice bi-directional traffic forwarding using threading
- Explore concurrent networking and low-level TCP data transmission
