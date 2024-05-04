#!/usr/bin/python3

import socket

# Dictionary to keep track of usernames and their assigned IPs and ports
user_ports = {}
# Dictionary to track active connections between users
connections = {}
start_port = 50000
BUFFER_SIZE = 2048

def handle_client_message(data, client_address, sock):
    message = data.decode()
    client_ip, client_port = client_address

    # Identifying the sender by matching IP and port
    sender = next((user for user, (ip, port) in user_ports.items() if ip == client_ip and port == client_port), None)

    if message.startswith("NAME"):
        username = message.split()[1]
        if username not in user_ports:
            assigned_port = start_port + len(user_ports)
            user_ports[username] = (client_ip, assigned_port)
            response = f"Hello {username}, you have been registered."
        else:
            response = "Error: This NAME is already taken."
    elif message.strip() == "LIST":
        if user_ports:
            user_list = ", ".join([f"{user}/{ip}:{port}" for user, (ip, port) in user_ports.items()])
            response = f"OK LIST = {user_list}"
        else:
            response = "No users registered."
    elif message.strip().startswith("CONN"):
        target = message.split()[1]
        if target in user_ports or sender:
            # Establish a direct connection between sender and target
            connections[sender] = user_ports[target]
            response = f"You are now connected to {target}."
        else:
            response = "Error: Target user does not exist or invalid sender."
    elif message.strip() == "QUIT":
        if sender in connections:
            del connections[sender]
            response = "OK Bye"
        else:
            response = "You are not connected."
    elif sender and sender in connections:
        # Relay messages to the connected user
        target_ip, target_port = connections[sender]
        sock.sendto(data.encode(), (target_ip, target_port))
        # Display the relayed message to confirm it was sent
        print(f"Message relayed to {sender}: {message}")
        return  # Prevent echoing back the message
    else:
        response = message  # Echo back non-command messages

    sock.sendto(response.encode(), client_address)

def receive_messages(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((server_ip, server_port))
        print(f"Server running on {server_ip}:{server_port}")
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            print(f"Received: {data.decode()}")  # Print message content for debugging
            handle_client_message(data, addr, sock)

if __name__ == "__main__":
    SERVER_IP = 'localhost'
    SERVER_PORT = 12345
    receive_messages(SERVER_IP, SERVER_PORT)
